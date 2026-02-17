# Deployment Guide

## Docker Deployment

### Build and Run with Docker

```bash
# Build the image
docker build -t ai-feasibility-engine .

# Run the container
docker run -d \
  --name feasibility-engine \
  -p 8000:8000 \
  --env-file .env \
  ai-feasibility-engine
```

### Using Docker Compose

```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

## Cloud Deployment

### Deploy to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `.env`
5. Deploy

### Deploy to Railway

1. Create a new project on Railway
2. Connect your GitHub repository
3. Add environment variables
4. Railway will auto-detect and deploy

### Deploy to Google Cloud Run

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/feasibility-engine

# Deploy to Cloud Run
gcloud run deploy feasibility-engine \
  --image gcr.io/PROJECT_ID/feasibility-engine \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GROQ_API_KEY=xxx,SUPABASE_URL=xxx,...
```

### Deploy to AWS ECS

1. Push image to ECR
2. Create ECS task definition
3. Create ECS service
4. Configure environment variables
5. Set up load balancer

## Production Considerations

### Environment Variables

Ensure all required environment variables are set:
- GROQ_API_KEY
- SUPABASE_URL
- SUPABASE_KEY
- SUPABASE_DB_URL

### Security

- Use HTTPS in production
- Implement rate limiting
- Add authentication/authorization
- Configure CORS appropriately
- Use secrets management (AWS Secrets Manager, Google Secret Manager, etc.)

### Monitoring

- Set up application monitoring (Sentry, DataDog, etc.)
- Configure logging aggregation
- Set up alerts for errors and performance issues

### Scaling

- Use horizontal scaling for high traffic
- Consider caching frequently requested analyses
- Implement request queuing for long-running analyses
- Use CDN for static assets

### Database

- Ensure Supabase is on a production plan
- Set up database backups
- Monitor database performance
- Consider read replicas for high read loads

### Performance Optimization

- Enable response compression
- Implement caching layer (Redis)
- Use connection pooling
- Optimize vector search indexes

## Health Checks

The application provides a health check endpoint at `/health`:

```bash
curl http://your-domain.com/health
```

## Continuous Deployment

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and push Docker image
        run: |
          docker build -t your-registry/feasibility-engine .
          docker push your-registry/feasibility-engine
      
      - name: Deploy to production
        run: |
          # Your deployment commands here
```

## Troubleshooting

### Container won't start
- Check environment variables are set correctly
- Verify database connection string
- Check logs: `docker logs feasibility-engine`

### High memory usage
- Reduce batch sizes
- Implement request queuing
- Scale horizontally

### Slow responses
- Check database query performance
- Verify LLM API latency
- Consider caching

## Support

For deployment issues, check:
1. Application logs
2. Database connectivity
3. API key validity
4. Network configuration
