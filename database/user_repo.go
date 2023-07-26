package database

import (
	"fmt"

	"github.com/google/uuid"
	"github.com/jmoiron/sqlx"
	"miauw.social/user"
)

type ProfileRepository struct {
	*sqlx.DB
}

func NewProfileRepository(db *sqlx.DB) *ProfileRepository {
	return &ProfileRepository{
		DB: db,
	}
}

func (s *ProfileRepository) Profile(id uuid.UUID) (user.Profile, error) {
	var u user.Profile
	if err := s.Get(&u, `select * from profiles where id = $1 and deleted_at is null;`, id); err != nil {
		return user.Profile{}, fmt.Errorf("Error getting profile: %w ", err)
	}
	return u, nil
}

func (s *ProfileRepository) Profiles() ([]user.Profile, error) {
	panic("not implemented") // TODO: Implement
}

func (s *ProfileRepository) CreateProfile(p *user.Profile) error {
	if err := s.Get(p, `insert into profiles values($1, $2, $3) returning *;`,
		p.ID,
		p.Username,
		p.EMail,
	); err != nil {
		return fmt.Errorf("Error creating profile: %w", err)
	}
	return nil
}

func (s *ProfileRepository) UpdateProfile(p *user.Profile) error {
	if err := s.Get(p, `update profiles set username = $1, email = $2 where id = $3 returning *;`,
		p.Username,
		p.EMail,
		p.ID,
	); err != nil {
		return fmt.Errorf("Error creating profile: %w", err)
	}
	return nil
}

func (s *ProfileRepository) DeleteProfile(id uuid.UUID) error {
	if _, err := s.Exec("update profiles set deleted_at = current_timestamp where id = $1", id); err != nil {
		return fmt.Errorf("error deleting profile: %w", err)
	}
	return nil
}
