import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.sql.*;
import java.text.SimpleDateFormat;
import java.util.Date;

public class ToDoListApp extends JFrame {
    private JTextField taskField, searchField;
    private JSpinner dateSpinner;
    private JTable taskTable;
    private DefaultTableModel model;
    private Connection conn;

    private static final String DB_URL = "jdbc:mysql://localhost:3306/";
    private static final String DB_NAME = "todo_app";
    private static final String USER = "root";
    private static final String PASS = "D$ai1919";

    public ToDoListApp() {
        setTitle("🌿 To-Do List Manager");
        setSize(950, 600);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        // === UI Fonts ===
        UIManager.put("Button.font", new Font("Segoe UI Emoji", Font.PLAIN, 14));
        UIManager.put("Label.font", new Font("Segoe UI Emoji", Font.PLAIN, 14));
        UIManager.put("Table.font", new Font("Segoe UI Emoji", Font.PLAIN, 14));

        JPanel mainPanel = new GradientPanel();
        mainPanel.setLayout(new BorderLayout(15, 15));
        mainPanel.setBorder(new EmptyBorder(15, 15, 15, 15));

        JLabel title = new JLabel("🌿 To-Do List Manager", SwingConstants.CENTER);
        title.setFont(new Font("Segoe UI Emoji", Font.BOLD, 26));
        title.setForeground(new Color(0, 90, 100));

        // ===== Top Panel =====
        JPanel topPanel = new JPanel(new BorderLayout());
        topPanel.setOpaque(false);

        // ===== Input Section =====
        JPanel inputPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 10));
        inputPanel.setOpaque(false);

        taskField = new JTextField(20);
        dateSpinner = new JSpinner(new SpinnerDateModel());
        JSpinner.DateEditor dateEditor = new JSpinner.DateEditor(dateSpinner, "yyyy-MM-dd");
        dateSpinner.setEditor(dateEditor);

        JButton addButton = styledButton("➕ Add Task", new Color(0, 180, 90));
        addButton.addActionListener(e -> addTask());

        inputPanel.add(new JLabel("Task:"));
        inputPanel.add(taskField);
        inputPanel.add(new JLabel("Due Date:"));
        inputPanel.add(dateSpinner);
        inputPanel.add(addButton);

        // ===== Search Section =====
        JPanel searchPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        searchPanel.setOpaque(false);
        searchField = new JTextField(15);

        JButton searchButton = styledButton("🔍 Search", new Color(60, 150, 255));
        searchButton.addActionListener(e -> searchTasks());
        JButton resetButton = styledButton("🔁 Reset", new Color(180, 180, 180));
        resetButton.addActionListener(e -> loadTasks());
        JButton historyButton = styledButton("📜 History", new Color(0, 160, 120));
        historyButton.addActionListener(e -> new HistoryPage(conn, this));

        searchPanel.add(searchField);
        searchPanel.add(searchButton);
        searchPanel.add(resetButton);
        searchPanel.add(historyButton);

        topPanel.add(inputPanel, BorderLayout.WEST);
        topPanel.add(searchPanel, BorderLayout.EAST);

        // ===== Table =====
        model = new DefaultTableModel(new Object[]{"ID", "Task", "Due Date", "Status"}, 0);
        taskTable = new JTable(model);
        taskTable.setRowHeight(30);
        taskTable.setBackground(new Color(245, 255, 245));
        taskTable.setSelectionBackground(new Color(200, 255, 220));
        taskTable.setSelectionForeground(Color.BLACK);
        taskTable.setGridColor(new Color(210, 230, 210));
        taskTable.setDefaultRenderer(Object.class, new TaskCellRenderer());

        JScrollPane scrollPane = new JScrollPane(taskTable);
        scrollPane.getViewport().setBackground(Color.WHITE);

        // ===== Bottom Buttons =====
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 15, 10));
        buttonPanel.setOpaque(false);

        JButton doneButton = styledButton("✅ Mark Done", new Color(0, 180, 90));
        JButton deleteButton = styledButton("🗑️ Delete", new Color(255, 80, 80));

        doneButton.addActionListener(e -> toggleDone());
        deleteButton.addActionListener(e -> deleteTask());

        buttonPanel.add(doneButton);
        buttonPanel.add(deleteButton);

        // ===== Assemble =====
        mainPanel.add(title, BorderLayout.NORTH);
        mainPanel.add(topPanel, BorderLayout.PAGE_START);
        mainPanel.add(scrollPane, BorderLayout.CENTER);
        mainPanel.add(buttonPanel, BorderLayout.SOUTH);

        add(mainPanel);

        connectAndSetupDB();
        loadTasks();
    }

    /** Connect to database and setup tables **/
    private void connectAndSetupDB() {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            try (Connection tempConn = DriverManager.getConnection(DB_URL, USER, PASS);
                 Statement stmt = tempConn.createStatement()) {
                stmt.executeUpdate("CREATE DATABASE IF NOT EXISTS " + DB_NAME);
            }

            conn = DriverManager.getConnection(DB_URL + DB_NAME, USER, PASS);
            try (Statement stmt = conn.createStatement()) {
                stmt.executeUpdate("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        task VARCHAR(255),
                        duedate DATE,
                        done BOOLEAN DEFAULT 0
                    )
                """);
                stmt.executeUpdate("""
                    CREATE TABLE IF NOT EXISTS task_history (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        task VARCHAR(255),
                        completed_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """);
            }
        } catch (Exception e) {
            JOptionPane.showMessageDialog(this, "❌ Database error: " + e.getMessage());
        }
    }

    /** Load all tasks **/
    public void loadTasks() {
        model.setRowCount(0);
        if (conn == null) {
            JOptionPane.showMessageDialog(this, "Database not connected!");
            return;
        }

        String sql = "SELECT * FROM tasks ORDER BY duedate ASC";
        try (Statement stmt = conn.createStatement(); ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                model.addRow(new Object[]{
                        rs.getInt("id"),
                        rs.getString("task"),
                        rs.getDate("duedate"),
                        rs.getBoolean("done") ? "✅ Done" : "❌ Pending"
                });
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    /** Add a new task **/
    private void addTask() {
        String task = taskField.getText().trim();
        if (task.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Please enter a task!");
            return;
        }

        Date date = (Date) dateSpinner.getValue();
        String dueDate = new SimpleDateFormat("yyyy-MM-dd").format(date);

        String sql = "INSERT INTO tasks(task, duedate, done) VALUES (?, ?, 0)";
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, task);
            ps.setString(2, dueDate);
            ps.executeUpdate();
            taskField.setText("");
            loadTasks();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    /** Search tasks **/
    private void searchTasks() {
        String keyword = searchField.getText().trim();
        if (keyword.isEmpty()) {
            loadTasks();
            return;
        }

        model.setRowCount(0);
        String sql = "SELECT * FROM tasks WHERE task LIKE ?";
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, "%" + keyword + "%");
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                model.addRow(new Object[]{
                        rs.getInt("id"),
                        rs.getString("task"),
                        rs.getDate("duedate"),
                        rs.getBoolean("done") ? "✅ Done" : "❌ Pending"
                });
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    /** Delete selected task **/
    private void deleteTask() {
        int row = taskTable.getSelectedRow();
        if (row == -1) {
            JOptionPane.showMessageDialog(this, "Select a task to delete!");
            return;
        }

        int id = (int) model.getValueAt(row, 0);
        try (PreparedStatement ps = conn.prepareStatement("DELETE FROM tasks WHERE id = ?")) {
            ps.setInt(1, id);
            ps.executeUpdate();
            loadTasks();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    /** Toggle task status (Pending/Done) **/
    private void toggleDone() {
        int row = taskTable.getSelectedRow();
        if (row == -1) {
            JOptionPane.showMessageDialog(this, "Select a task to mark done!");
            return;
        }

        int id = (int) model.getValueAt(row, 0);
        String currentStatus = (String) model.getValueAt(row, 3);
        boolean newStatus = currentStatus.contains("❌");

        try {
            String updateSQL = "UPDATE tasks SET done = ? WHERE id = ?";
            try (PreparedStatement ps = conn.prepareStatement(updateSQL)) {
                ps.setBoolean(1, newStatus);
                ps.setInt(2, id);
                ps.executeUpdate();
            }

            if (newStatus) {
                String selectSQL = "SELECT task FROM tasks WHERE id = ?";
                try (PreparedStatement ps = conn.prepareStatement(selectSQL)) {
                    ps.setInt(1, id);
                    ResultSet rs = ps.executeQuery();
                    if (rs.next()) {
                        String task = rs.getString("task");
                        String insertSQL = "INSERT INTO task_history(task) VALUES (?)";
                        try (PreparedStatement ps2 = conn.prepareStatement(insertSQL)) {
                            ps2.setString(1, task);
                            ps2.executeUpdate();
                        }
                    }
                }
            }
            loadTasks();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    /** Styled buttons **/
    private JButton styledButton(String text, Color bg) {
        JButton button = new JButton(text);
        button.setFocusPainted(false);
        button.setForeground(Color.WHITE);
        button.setBackground(bg);
        button.setFont(new Font("Segoe UI Emoji", Font.BOLD, 14));
        button.setBorder(BorderFactory.createEmptyBorder(8, 18, 8, 18));
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));
        return button;
    }

    /** Gradient background **/
    static class GradientPanel extends JPanel {
        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2d = (Graphics2D) g;
            Color c1 = new Color(210, 255, 240);
            Color c2 = new Color(180, 220, 255);
            g2d.setPaint(new GradientPaint(0, 0, c1, 0, getHeight(), c2));
            g2d.fillRect(0, 0, getWidth(), getHeight());
        }
    }

    /** Table color styling **/
    static class TaskCellRenderer extends DefaultTableCellRenderer {
        @Override
        public Component getTableCellRendererComponent(JTable table, Object value,
                                                       boolean isSelected, boolean hasFocus, int row, int col) {
            Component c = super.getTableCellRendererComponent(table, value, isSelected, hasFocus, row, col);
            c.setFont(new Font("Segoe UI Emoji", Font.PLAIN, 14));
            try {
                Date due = (Date) table.getModel().getValueAt(row, 2);
                String status = (String) table.getModel().getValueAt(row, 3);
                if (status.contains("✅")) c.setForeground(new Color(0, 180, 90));
                else if (status.contains("❌") && due.before(new Date()))
                    c.setForeground(new Color(255, 100, 80));
                else c.setForeground(Color.BLACK);
                if (isSelected) c.setForeground(Color.BLUE);
            } catch (Exception ignored) {}
            return c;
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new ToDoListApp().setVisible(true));
    }
}

/** 📜 HISTORY PAGE **/
class HistoryPage extends JFrame {
    private JTable historyTable;
    private DefaultTableModel historyModel;
    private final ToDoListApp parent;

    public HistoryPage(Connection conn, ToDoListApp parent) {
        this.parent = parent;
        setTitle("📜 Completed Task History");
        setSize(700, 400);
        setLocationRelativeTo(null);

        JPanel panel = new ToDoListApp.GradientPanel();
        panel.setLayout(new BorderLayout(10, 10));
        panel.setBorder(new EmptyBorder(15, 15, 15, 15));

        JLabel title = new JLabel("📜 Completed Task History", SwingConstants.CENTER);
        title.setFont(new Font("Segoe UI Emoji", Font.BOLD, 22));
        title.setForeground(new Color(0, 100, 100));

        historyModel = new DefaultTableModel(new Object[]{"Task", "Completed On"}, 0);
        historyTable = new JTable(historyModel);
        historyTable.setRowHeight(28);
        historyTable.setFont(new Font("Segoe UI Emoji", Font.PLAIN, 14));
        historyTable.setBackground(new Color(245, 255, 255));
        JScrollPane scrollPane = new JScrollPane(historyTable);

        panel.add(title, BorderLayout.NORTH);
        panel.add(scrollPane, BorderLayout.CENTER);
        add(panel);

        loadHistory(conn);
        setVisible(true);
    }

    private void loadHistory(Connection conn) {
        historyModel.setRowCount(0);
        try (Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT task, completed_on FROM task_history ORDER BY completed_on DESC")) {
            while (rs.next()) {
                historyModel.addRow(new Object[]{
                        rs.getString("task"),
                        rs.getTimestamp("completed_on")
                });
            }
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, "❌ Error loading history: " + e.getMessage());
        }
    }
}
