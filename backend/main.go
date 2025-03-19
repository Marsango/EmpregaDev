package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"net/http"
	"time"

	"github.com/joho/godotenv"
	"github.com/jackc/pgx/v5/pgxpool"
    "github.com/gin-gonic/gin"
	"github.com/gin-contrib/cors"
	
)

var db *pgxpool.Pool

type Job struct {
		ID             int       `json:"id"`
		Name           string    `json:"name"`
		Company        string    `json:"company"`
		PublishedDate  time.Time `json:"published_date"`
		DeadLineDate   time.Time `json:"dead_line_date"`
		IsRemote       bool      `json:"is_remote"`
		Url            string    `json:"url"`
		Website        string    `json:"website"`	
}

func createDatabaseConnection() error {
	if err := godotenv.Load(); err != nil {
		log.Println("Warning: Error loading .env file (default values may be used)")
	}

	host := os.Getenv("HOST")
	port := os.Getenv("PORT")
	user := os.Getenv("USER")
	dbName := os.Getenv("DB_NAME")
	password := os.Getenv("PASSWORD")

	dbUrl := fmt.Sprintf("postgres://%s:%s@%s:%s/%s", user, password, host, port, dbName)

	var err error
	db, err = pgxpool.New(context.Background(), dbUrl)
	if err != nil {
		return fmt.Errorf("unable to connect to database: %w", err)
	}

	fmt.Println("Connected to the database successfully!")
	return nil
}

func main() {
	if err := createDatabaseConnection(); err != nil {
		log.Fatal(err)
	}

	defer db.Close()

	router := gin.Default()
	router.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:5173"},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Length", "Content-Type"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))
	router.GET("/jobs", getJobs)
	router.Run("localhost:8080")
}

func getJobs(c *gin.Context){
	rows, err := db.Query(context.Background(), "SELECT id, name, company, published_date, dead_line_date, is_remote, url, website from available_job ORDER BY published_date DESC")
	if err != nil {
        c.IndentedJSON(http.StatusBadRequest, gin.H{"error": err})
		return
    }
	defer rows.Close()

	var jobs []Job
	for rows.Next() {
        var job Job
        if err := rows.Scan(&job.ID, &job.Name, &job.Company, &job.PublishedDate, &job.DeadLineDate, &job.IsRemote, &job.Url, &job.Website); err != nil {
            fmt.Println("Erro ao escanear job:", err)
			continue
        }
        jobs = append(jobs, job)
    }
    c.IndentedJSON(http.StatusOK, jobs)
}

