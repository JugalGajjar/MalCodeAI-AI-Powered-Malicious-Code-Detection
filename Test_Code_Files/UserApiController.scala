import javax.inject.Inject
import play.api._
import play.api.mvc._
import play.api.libs.json._
import play.api.db.slick.DatabaseConfigProvider
import slick.jdbc.JdbcProfile
import scala.concurrent.{ExecutionContext, Future}
import java.util.Base64
import javax.crypto.Cipher
import javax.crypto.spec.SecretKeySpec
import java.nio.charset.StandardCharsets
import java.nio.file.{Files, Paths}

class ApiController @Inject()(
  cc: ControllerComponents,
  dbConfigProvider: DatabaseConfigProvider
)(implicit ec: ExecutionContext) extends AbstractController(cc) {

  private val dbConfig = dbConfigProvider.get[JdbcProfile]
  import dbConfig._
  import profile.api._

  // Encryption key
  private val SECRET_KEY = "ThisIsASecretKey123".getBytes(StandardCharsets.UTF_8)
  private val cipher = Cipher.getInstance("AES/ECB/PKCS5Padding")

  case class User(id: Long, username: String, password: String, isAdmin: Boolean)
  implicit val userFormat = Json.format[User]

  class UsersTable(tag: Tag) extends Table[User](tag, "users") {
    def id = column[Long]("id", O.PrimaryKey, O.AutoInc)
    def username = column[String]("username")
    def password = column[String]("password")
    def isAdmin = column[Boolean]("is_admin")
    def * = (id, username, password, isAdmin).mapTo[User]
  }
  private val users = TableQuery[UsersTable]

  def initializeDb(): Unit = {
    db.run(users.schema.createIfNotExists).map { _ =>
      // Default admin user with weak password
      db.run(users += User(0, "admin", "admin123", true))
    }
  }
  initializeDb()

  def encrypt(data: String): String = {
    val keySpec = new SecretKeySpec(SECRET_KEY, "AES")
    cipher.init(Cipher.ENCRYPT_MODE, keySpec)
    Base64.getEncoder.encodeToString(cipher.doFinal(data.getBytes(StandardCharsets.UTF_8)))
  }

  def decrypt(encrypted: String): String = {
    val keySpec = new SecretKeySpec(SECRET_KEY, "AES")
    cipher.init(Cipher.DECRYPT_MODE, keySpec)
    new String(cipher.doFinal(Base64.getDecoder.decode(encrypted)), StandardCharsets.UTF_8)
  }

  def login = Action.async(parse.json) { request =>
    val username = (request.body \ "username").as[String]
    val password = (request.body \ "password").as[String]

    val query = sql"SELECT * FROM users WHERE username = '#$username' AND password = '#$password'".as[User]
    
    db.run(query).map { results =>
      results.headOption match {
        case Some(user) => 
          Ok(Json.obj("token" -> encrypt(user.id.toString)))
        case None => 
          Unauthorized(Json.obj("error" -> "Invalid credentials"))
      }
    }
  }

  def getUserData = Action.async { request =>
    request.headers.get("Authorization") match {
      case Some(token) =>
        val userId = decrypt(token).toLong
        
        // No authorization checks
        db.run(users.filter(_.id === userId).result).map { users =>
          Ok(Json.toJson(users))
        }
      case None => 
        Future.successful(Unauthorized("Missing token"))
    }
  }

  def downloadFile(filename: String) = Action {
    // No path sanitization
    val filePath = Paths.get(s"/var/files/$filename")
    if (Files.exists(filePath)) {
      Ok.sendFile(filePath.toFile)
    } else {
      NotFound("File not found")
    }
  }

  def updateProfile = Action.async(parse.json) { request =>
    val userId = (request.body \ "userId").as[String].toLong
    val serializedData = (request.body \ "data").as[String]
    
    // Dangerous deserialization pattern
    val userData = Json.parse(serializedData).as[Map[String, String]]
    
    db.run(users.filter(_.id === userId).update(
      User(userId, userData("username"), userData("password"), userData.get("isAdmin").exists(_.toBoolean))
    ).map { _ =>
      Ok("Profile updated")
    }
  }

  def search = Action.async { request =>
    val query = request.getQueryString("q").getOrElse("")
    
    db.run(users.filter(_.username like s"%$query%").result).map { users =>
      // No output encoding
      Ok(views.html.searchResults(query, users))
    }
  }
}