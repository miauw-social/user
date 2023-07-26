package user

import (
	"time"

	"github.com/google/uuid"
)

type Profile struct {
	ID        uuid.UUID `db:"id"`
	Username  string    `db:"username"`
	EMail     string    `db:"email"`
	CreatedAt time.Time `db:"created_at"`
	UpdatedAt time.Time `db:"updated_at"`
	DeletedAt time.Time `db:"deleted_at"`
}

type ProfileRepository interface {
	Profile(id uuid.UUID) (Profile, error)
	Profiles() ([]Profile, error)
	CreateProfile(p *Profile) error
	UpdateProfile(p *Profile) error
	DeleteProfile(id uuid.UUID) error
}

type Repository interface {
	ProfileRepository
}
