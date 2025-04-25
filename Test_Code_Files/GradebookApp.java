import java.util.*;
import java.io.*;

class Student {
    private int id;
    private String name;
    private Map<String, Double> grades;

    public Student(int id, String name) {
        this.id = id;
        this.name = name;
        this.grades = new HashMap<>();
    }

    public int getId() { return id; }
    public String getName() { return name; }

    public void addGrade(String subject, double grade) {
        if (grade < 0 || grade > 100) {
            System.out.println("Invalid grade for " + subject + ". Must be between 0 and 100.");
            return;
        }
        grades.put(subject, grade);
    }

    public Double getGrade(String subject) {
        return grades.get(subject);
    }

    public double getAverage() {
        return grades.values().stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
    }

    public String generateReport() {
        StringBuilder sb = new StringBuilder();
        sb.append("ID: ").append(id).append(" | Name: ").append(name).append("\n");
        for (var entry : grades.entrySet()) {
            sb.append("  ").append(entry.getKey()).append(": ").append(entry.getValue()).append("\n");
        }
        sb.append(String.format("  Average: %.2f\n", getAverage()));
        return sb.toString();
    }

    public void printReport() {
        System.out.print(generateReport());
    }
}

class Gradebook {
    private List<Student> students;

    public Gradebook() {
        students = new ArrayList<>();
    }

    public void addStudent(Student s) {
        students.add(s);
    }

    public void printAllReports() {
        for (Student s : students) {
            s.printReport();
            System.out.println("----------------------");
        }
    }

    public Student findStudentById(int id) {
        for (Student s : students) {
            if (s.getId() == id) return s;
        }
        return null;
    }

    public void sortStudentsByAverage() {
        students.sort((a, b) -> Double.compare(b.getAverage(), a.getAverage()));
    }

    public void exportReportsToFile(String filename) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            for (Student s : students) {
                writer.write(s.generateReport());
                writer.write("----------------------\n");
            }
            System.out.println("Reports exported to " + filename);
        } catch (IOException e) {
            System.out.println("Error exporting reports: " + e.getMessage());
        }
    }
}

public class GradebookApp {
    public static void main(String[] args) {
        Gradebook gradebook = new Gradebook();

        Student s1 = new Student(101, "Alice");
        s1.addGrade("Math", 88);
        s1.addGrade("Science", 92);

        Student s2 = new Student(102, "Bob");
        s2.addGrade("Math", 75);
        s2.addGrade("Science", 80);
        s2.addGrade("History", 85);

        Student s3 = new Student(103, "Charlie");
        s3.addGrade("Math", 95);
        s3.addGrade("Art", 100);

        gradebook.addStudent(s1);
        gradebook.addStudent(s2);
        gradebook.addStudent(s3);

        System.out.println("📊 All Reports:");
        gradebook.printAllReports();

        System.out.println("📈 Sorted by Average:");
        gradebook.sortStudentsByAverage();
        gradebook.printAllReports();

        System.out.println("🔍 Grade Lookup:");
        Student target = gradebook.findStudentById(102);
        if (target != null) {
            System.out.println("Bob's History Grade: " + target.getGrade("History"));
        }

        gradebook.exportReportsToFile("student_reports.txt");
    }
}