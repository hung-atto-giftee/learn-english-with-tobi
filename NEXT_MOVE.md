# Next Move: Bringing the Project to 10/10 Perfection Level

This document is a roadmap to take `Study English With Tobi` from its current MVP state to a highly polished level from product, technical, and operational perspectives.

The goal is not to "add tons of features", but to make it:
- More stable
- More scalable
- More maintainable
- Better learning experience
- Ready for real users

## 1. Current Assessment

The project already has a very good foundation:
- FastAPI backend
- React frontend
- JWT auth
- TTS
- Dictation evaluation
- Learning history
- Dictionary + vocabulary
- Docker
- CI check install Python packages

Current levels can be considered:
- `Good MVP`: `7/10`
- `Ready for small users`: `6.5/10`
- `Production ready`: `5.5/10`

To reach `10/10`, need to go through 4 layers:
1. Stability and code quality
2. Product and UX
3. Security and operations
4. Scale and analytics

## 2. Priority Order to Reach 10/10

If you only have limited time, follow this order:

1. Testing and code quality
2. Auth security and API
3. Database migration + backup strategy
4. Logging, monitoring, error tracking
5. UX/product polish
6. Background jobs + storage strategy
7. Analytics and recommendations

## 3. Phase 1: Bring to 8/10 Level

This is the phase with the highest ROI. Should be done first.

### 3.1. Add Backend Testing

Objective:
- Prevent app breakage when adding new features

Need to have:
- Unit tests for `evaluator.py`
- Unit tests for `dictionary/service.py`
- API tests for:
  - `/auth/register`
  - `/auth/login`
  - `/practice`
  - `/evaluate`
  - `/history`
  - `/dictionary`

Tools:
- `pytest`
- `httpx.AsyncClient`
- Separate test DB

Definition of done:
- Have CI workflow running backend tests
- Pushing code doesn't break main routes

### 3.2. Add Frontend Testing

Need to have:
- Render tests for login page
- Render tests for practice flow
- Interaction tests for dictionary modal
- Test route protection

Tools:
- `vitest`
- `@testing-library/react`

Definition of done:
- Have CI workflow checking `npm run build`
- Have tests for main flows

### 3.3. Refactor Configuration Structure

Objective:
- Clearly separate config by environment

Need to do:
- Create `settings.py` or separate config module
- Validate required env variables
- Separate:
  - dev
  - test
  - production

Should have:
- `APP_ENV`
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `CORS_ORIGINS`

### 3.4. Upgrade Error Handling

Need to do:
- Global exception handler for FastAPI
- Unified error response format
- Frontend shows more user-friendly errors

Desired example:
```json
{
  "error": {
    "code": "dictionary_lookup_failed",
    "message": "Could not load dictionary data."
  }
}
```

## 4. Phase 2: Bring to 8.5/10 Level

### 4.1. Better Auth Security

Need to do:
- Refresh tokens
- Logout all sessions
- Email verification
- Forgot password / reset password
- Rate limit login
- Temporary lock if too many failed logins

Suggested tools:
- Redis for session/rate limiting
- Email service like Resend, SendGrid, Postmark

### 4.2. Reduce Public API Risks

Need to do:
- Rate limit `/dictionary`
- Rate limit `/tts`
- Limit input paragraph length
- More careful validation of files/paths/words

### 4.3. User Permissions and Profiles

Need to add:
- Profile endpoint
- Avatar/display name
- Role `user/admin`

Will be very useful later when:
- Have admin dashboard
- Have moderation
- Have content library

## 5. Phase 3: Bring to 9/10 Level

### 5.1. Proper Database Migration

Currently creating tables with startup code. This is fine for MVP, but not good for large production.

Need to upgrade:
- Use Alembic
- Version schema
- Clear migration rollback

Definition of done:
- All schema changes go through migrations
- Have migrations for:
  - users
  - learning_history
  - user_word_history
  - dictionary cache if needed

### 5.2. Separate Dictionary Cache from Local SQLite

Currently SQLite is very reasonable for local use. But if deploying multiple instances, local cache will be separated.

10/10 direction:
- Use PostgreSQL for cache metadata
- Or Redis for fast cache
- Or separate storage layer for dictionary cache

### 5.3. Production-Ready Audio Storage

Currently audio files are saved to local filesystem.

Need to upgrade:
- Save on S3-compatible storage
- Have cleanup policy
- Have cache headers
- Avoid saving duplicate files

Tools:
- AWS S3
- Cloudflare R2
- MinIO

## 6. Phase 4: Bring to 9.5/10 Level

### 6.1. Monitoring and Logging

Need to have:
- Structured logging
- Request ID
- Track latency
- Track error rate
- Alert when API has many errors

Tools:
- Sentry
- Grafana
- Prometheus
- Better Stack or ELK

Definition of done:
- Know which routes are slow
- Know which APIs have errors
- Know where users encounter errors

### 6.2. Background Jobs

TTS and some other tasks should be moved to background for high scale.

Need to do:
- Queue job to generate audio
- Pre-generate audio for lessons
- Retry job if edge-tts fails

Tools:
- Celery
- RQ
- Dramatiq

### 6.3. Production Docker and Deploy

Need to have:
- Multi-stage Docker build
- Production compose or Kubernetes later
- Reverse proxy like Nginx / Traefik
- HTTPS
- Real domain

Definition of done:
- 1 command deploy
- Easy rollback
- Complete logs and healthcheck

## 7. Phase 5: Bring to 10/10 Product Level

This is the part that turns the app into a very strong English learning product.

### 7.1. Real Lesson System

Need to do:
- Content library
- Levels A1/A2/B1/B2
- Lesson tags
- Topics: travel, work, daily life
- Generated lesson packs

### 7.2. Smarter Learning

Need to do:
- Spaced repetition for vocabulary
- Review words with many mistakes
- Review sentences with low accuracy
- Suggest next lessons

### 7.3. User Dashboard

Need to have:
- Learning streak
- Weekly accuracy
- Words learned
- Time spent
- Strongest / weakest topics

### 7.4. Social / Gamification

If wanting to increase retention:
- Badges
- XP
- Small leaderboard
- Daily goals
- 7-day challenges

### 7.5. Mobile-First

Should consider:
- More responsive design
- PWA
- Mobile app React Native or Flutter later

## 8. UX Upgrades to Reach 10/10

### 8.1. Practice UX

Need to add:
- Auto next sentence
- Keyboard shortcuts
- Replay hotkey
- Show/hide transcript
- Configurable repeat count

### 8.2. Dictionary UX

Need to add:
- Save favorite words
- Grouped meanings
- Example sentences
- Word audio speed options
- Recent lookups panel

### 8.3. History UX

Need to add:
- Better charts
- Filter by date range
- Search by sentence
- Export CSV
- Compare this week vs last week

## 9. DevOps 10/10 Level

### 9.1. Complete CI/CD

Need to have:
- Python test workflow
- Frontend build workflow
- Lint workflow
- Docker build workflow
- Deploy workflow

### 9.2. Secrets and Config

Need to have:
- Secret manager
- Rotate JWT secret
- Separate env for staging / production

### 9.3. Backup and Recovery

Need to have:
- Regular PostgreSQL backup
- Regular restore testing
- Object storage retention policy

## 10. Most Specific Backlog to Start Right Away

If you want to move fast, here's a backlog of 10 things to start right away:

1. Add `pytest` for backend
2. Add `vitest` + `testing-library` for frontend
3. Add CI workflow for frontend build
4. Refactor env/config into separate module
5. Add global error handling
6. Add refresh token
7. Switch to Alembic migration
8. Move audio to object storage
9. Add Sentry
10. Add better learning dashboard

## 11. 30-Day Plan to Get Close to 10/10

### Week 1

- Backend tests
- Frontend build workflow
- Basic frontend tests
- Code quality cleanup

### Week 2

- Refresh token
- Reset password
- Rate limiting
- Global error handling

### Week 3

- Alembic migration
- S3/R2 audio storage
- Logging + Sentry

### Week 4

- User dashboard
- Review mistakes
- Vocabulary favorites
- Production deploy checklist

## 12. Definition of 10/10 for This Project

Project reaches 10/10 level when:
- Users can register, learn, look up words, view history smoothly
- App doesn't break when encountering external API errors
- Have tests and CI protecting code
- Have clear monitoring and logging
- Stable production deployment
- Have analytics and retention features
- Can scale at least for real user groups

## 13. Conclusion

This project already has a very good foundation. To reach 10/10, you don't need to rewrite from scratch.

You just need to follow the direction of:
- Strengthening the foundation
- Upgrading security
- Standardizing operations
- Deepening learning experience

If you choose the right order, after just a few more phases this project can reach very strong levels in both technical and product value.
