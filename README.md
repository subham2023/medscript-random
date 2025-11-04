# MedScript AI - Frontend
This directory contains the React/TypeScript frontend for the MedScript AI
application..
## Local Development
### Prerequisites
- Node.js (v18 or later)
- npm or yarn
### Setup
1. **Install dependencies:**
 ```bash
 npm install
 ```
2. **Set Environment Variables:**
 Create a `.env.development.local` file in the `frontend` directory. Set
the `REACT_APP_API_BASE_URL` to point to your locally running backend.
 ```
 REACT_APP_API_BASE_URL=http://localhost:8000/api/v1
 ```
### Running the Application
```bash
npm start
