# Eval Scenario Quality Review

## Problem Description

You have just downloaded three eval scenarios generated from recent commits. Before running evals, you need to review each scenario for quality issues that would make the eval results unreliable or misleading.

Common anti-patterns in generated scenarios include:
- **Answer leakage:** The task prompt gives away specific values or approaches that the rubric then checks for, turning criteria into free points rather than tests of agent capability.
- **Double-counting:** Two or more criteria reward the same underlying behavior, inflating scores for a single correct action.
- **Free points:** A criterion that any reasonable response would satisfy regardless of quality, providing no signal about agent capability.

Review each of the three scenarios below and identify any quality issues.

## What to produce

Write a `scenario-review.md` file that:
1. For each scenario, states whether it passes quality review or has issues
2. For each issue found, names the specific anti-pattern, quotes the problematic content, and explains why it's a problem
3. Proposes a concrete fix for each issue

## Scenarios

### Scenario 1: api-rate-limiter

=============== FILE: evals/api-rate-limiter/task.md ===============
# Implement API Rate Limiting

## Problem Description

Your team's API has been experiencing abuse from automated clients sending thousands of requests per second. The existing Express.js application has no rate limiting. You need to add rate limiting middleware that protects the API without impacting legitimate users.

The application uses Express 4.x with an existing middleware chain: CORS, body parser, auth, then route handlers. The rate limiter should be added to this chain.

## What to produce

Add rate limiting to the Express application:
- Create a rate limiting middleware in `src/middleware/rate-limiter.ts`
- Configure it with appropriate limits for the API
- Integrate it into the existing middleware chain
- Handle rate-limited requests gracefully with proper HTTP responses

## Input Files

=============== FILE: inputs/src/app.ts ===============
import express from 'express';
import cors from 'cors';
import { authMiddleware } from './middleware/auth';
import { apiRouter } from './routes/api';

const app = express();

app.use(cors());
app.use(express.json());
app.use(authMiddleware);
app.use('/api', apiRouter);

export default app;
=============== END FILE ===============

=============== FILE: evals/api-rate-limiter/criteria.json ===============
{
  "type": "weighted_checklist",
  "checklist": [
    {
      "name": "Rate limiter middleware created",
      "max_score": 15,
      "description": "A new rate limiting middleware file exists at src/middleware/rate-limiter.ts"
    },
    {
      "name": "Sliding window or token bucket algorithm",
      "max_score": 20,
      "description": "The rate limiter uses a sliding window or token bucket algorithm rather than a simple counter reset"
    },
    {
      "name": "429 status code returned",
      "max_score": 15,
      "description": "Rate-limited requests receive HTTP 429 Too Many Requests response"
    },
    {
      "name": "Middleware ordering correct",
      "max_score": 20,
      "description": "Rate limiter is placed after CORS and body parser but before auth middleware in the chain"
    },
    {
      "name": "Retry-After header included",
      "max_score": 15,
      "description": "Rate-limited responses include a Retry-After header indicating when the client can retry"
    },
    {
      "name": "Configurable limits",
      "max_score": 15,
      "description": "Rate limits (requests per window, window duration) are configurable rather than hardcoded"
    }
  ]
}
=============== END FILE ===============

---

### Scenario 2: config-migration

=============== FILE: evals/config-migration/task.md ===============
# Migrate Configuration from YAML to TOML

## Problem Description

Your team is standardizing on TOML for all configuration files. You need to migrate the application's main configuration from YAML to TOML format.

The current YAML config is at `config/app.yaml`. The migrated TOML config should be written to `config/app.toml`. You also need to update the config loader in `src/config/loader.ts` to read TOML instead of YAML.

The TOML output should:
- Use the `@iarna/toml` package (already in package.json) with `TOML.parse()` for reading
- Place database settings under a `[database]` table
- Place Redis settings under a `[cache]` table
- Place logging settings under a `[logging]` table
- Set the top-level key `format_version = 2`

## What to produce

1. Create `config/app.toml` with the migrated configuration
2. Update `src/config/loader.ts` to read from the TOML file
3. Remove or rename the old YAML file

## Input Files

=============== FILE: inputs/config/app.yaml ===============
app:
  name: platform-api
  port: 3000
  environment: production

database:
  host: db.internal.acme.com
  port: 5432
  name: platform
  pool_size: 20

cache:
  host: redis.internal.acme.com
  port: 6379
  ttl: 3600

logging:
  level: info
  format: json
  output: stdout
=============== END FILE ===============

=============== FILE: inputs/src/config/loader.ts ===============
import * as yaml from 'js-yaml';
import * as fs from 'fs';

export function loadConfig() {
  const raw = fs.readFileSync('config/app.yaml', 'utf-8');
  return yaml.load(raw) as Record<string, unknown>;
}
=============== END FILE ===============

=============== FILE: evals/config-migration/criteria.json ===============
{
  "type": "weighted_checklist",
  "checklist": [
    {
      "name": "TOML file created with correct structure",
      "max_score": 20,
      "description": "config/app.toml exists with [database], [cache], and [logging] tables containing the migrated values"
    },
    {
      "name": "Uses @iarna/toml package",
      "max_score": 15,
      "description": "The updated loader imports and uses @iarna/toml with TOML.parse() to read the config"
    },
    {
      "name": "Format version key present",
      "max_score": 15,
      "description": "The TOML file includes format_version = 2 as a top-level key"
    },
    {
      "name": "Database section uses TOML table",
      "max_score": 15,
      "description": "Database settings are under a [database] TOML table with host, port, name, and pool_size keys"
    },
    {
      "name": "Loader reads correct file path",
      "max_score": 15,
      "description": "The config loader reads from 'config/app.toml' instead of 'config/app.yaml'"
    },
    {
      "name": "Old YAML file handled",
      "max_score": 20,
      "description": "The old config/app.yaml is either deleted or renamed to indicate it's deprecated"
    }
  ]
}
=============== END FILE ===============

---

### Scenario 3: error-boundary-component

=============== FILE: evals/error-boundary-component/task.md ===============
# Add Error Boundary Components to React Application

## Problem Description

Your React application currently has no error boundaries. When a component throws during rendering, the entire app crashes to a white screen. You need to add error boundary components that catch rendering errors and display fallback UIs.

The application uses React 18 with TypeScript. There are two main areas that need protection: the top-level app shell and individual route-level page components.

## What to produce

1. Create a reusable `ErrorBoundary` component in `src/components/ErrorBoundary.tsx`
2. Create a user-friendly fallback UI component in `src/components/ErrorFallback.tsx`
3. Wrap the app's route outlet with the error boundary
4. Add error reporting to an external service when errors are caught

## Input Files

=============== FILE: inputs/src/App.tsx ===============
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Header } from './components/Header';
import { Dashboard } from './pages/Dashboard';
import { Settings } from './pages/Settings';
import { Profile } from './pages/Profile';

export function App() {
  return (
    <BrowserRouter>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
=============== END FILE ===============

=============== FILE: evals/error-boundary-component/criteria.json ===============
{
  "type": "weighted_checklist",
  "checklist": [
    {
      "name": "ErrorBoundary uses componentDidCatch",
      "max_score": 15,
      "description": "The ErrorBoundary is a class component that implements componentDidCatch lifecycle method for catching render errors"
    },
    {
      "name": "ErrorBoundary uses getDerivedStateFromError",
      "max_score": 15,
      "description": "The ErrorBoundary implements static getDerivedStateFromError to update state and trigger fallback rendering"
    },
    {
      "name": "Fallback UI is user-friendly",
      "max_score": 10,
      "description": "The ErrorFallback component displays a helpful message and offers a way to recover (e.g., retry button or link to home)"
    },
    {
      "name": "Error boundary wraps routes",
      "max_score": 15,
      "description": "The error boundary wraps the Routes component or route outlet in App.tsx so route-level crashes are caught"
    },
    {
      "name": "Error reporting to external service",
      "max_score": 15,
      "description": "Caught errors are reported to an external error tracking service (e.g., Sentry, Datadog, or a custom endpoint)"
    },
    {
      "name": "No unrelated changes",
      "max_score": 5,
      "description": "The solution does not modify files or components unrelated to error boundary functionality"
    },
    {
      "name": "Reusable component design",
      "max_score": 10,
      "description": "The ErrorBoundary accepts a fallback prop or render prop, making it reusable across different parts of the app"
    },
    {
      "name": "Error boundary catches rendering errors",
      "max_score": 15,
      "description": "The ErrorBoundary component correctly catches errors thrown during rendering of its children"
    }
  ]
}
=============== END FILE ===============
