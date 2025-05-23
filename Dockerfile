# Create a Jekyll container from a Ruby Alpine image

# At a minimum, use Ruby 2.5 or later
FROM ruby:3.4-alpine3.15

WORKDIR /srv/jekyll

# Add Jekyll dependencies to Alpine
RUN apk update
RUN apk add --no-cache build-base gcc cmake git

COPY ./Gemfile* /srv/jekyll

# Update the Ruby bundler and install Jekyll
RUN gem update bundler && bundle install
