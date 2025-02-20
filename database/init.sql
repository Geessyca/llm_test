CREATE TABLE IF NOT EXISTS qa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    feedback ENUM('positivo', 'negativo') DEFAULT NULL
);
