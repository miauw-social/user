FROM golang:1.20.6 as build
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . ./
RUN CGO_ENABLED=0 GOOS=linux go build -o /service


FROM alpine:latest
WORKDIR /app
COPY --from=build /service /app/service
ENV DB_HOST="localhost"
ENV DB_PORT=5432
ENV DB_USER="miauw"
ENV DB_PASS="password"
ENV DB_NAME="miauw"
CMD ["/app/service"]