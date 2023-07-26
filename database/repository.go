package database

import (
	"fmt"

	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"miauw.social/user"
)

type Repository struct {
	user.ProfileRepository
}

func NewRepository(dataSourceName string) (*Repository, error) {
	db, err := sqlx.Open("postgres", dataSourceName)
	if err != nil {
		return nil, fmt.Errorf("Error connecting to database: %w", err)
	}
	if err := db.Ping(); err != nil {
		return nil, fmt.Errorf("Error connecting to database: %w", err)
	}
	return &Repository{
		ProfileRepository: NewProfileRepository(db),
	}, nil
}
