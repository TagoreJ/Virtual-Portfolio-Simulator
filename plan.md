# Portfolio Management System - Enhanced with Authentication

## Overview
Building a feature-complete virtual stock trading platform with Google OAuth authentication, user account management, and Supabase integration for persistent data storage. Each new user starts with ₹1,00,000 virtual currency and builds their portfolio from scratch.

---

## 🔴 CRITICAL: Database Setup Required

Before the application can work, you MUST create the database tables in Supabase:

### Step 1: Go to Supabase SQL Editor
1. Visit https://supabase.com/dashboard
2. Select your project
3. Navigate to **SQL Editor** in the left sidebar
4. Click **New Query**

### Step 2: Execute this SQL to create all tables:

```sql
-- Create users table
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create portfolios table
CREATE TABLE IF NOT EXISTS portfolios (
    id SERIAL PRIMARY KEY,
    user_id TEXT REFERENCES users(user_id) ON DELETE CASCADE,
    available_cash DECIMAL(15, 2) DEFAULT 100000.00,
    total_value DECIMAL(15, 2) DEFAULT 100000.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- Create holdings table
CREATE TABLE IF NOT EXISTS holdings (
    id SERIAL PRIMARY KEY,
    user_id TEXT REFERENCES users(user_id) ON DELETE CASCADE,
    ticker TEXT NOT NULL,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    avg_price DECIMAL(15, 2) NOT NULL,
    current_price DECIMAL(15, 2) DEFAULT 0,
    day_change_pct DECIMAL(10, 4) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, ticker)
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    user_id TEXT REFERENCES users(user_id) ON DELETE CASCADE,
    ticker TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('BUY', 'SELL')),
    quantity INTEGER NOT NULL,
    price DECIMAL(15, 2) NOT NULL,
    total DECIMAL(15, 2) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create watchlist table
CREATE TABLE IF NOT EXISTS watchlist (
    id SERIAL PRIMARY KEY,
    user_id TEXT REFERENCES users(user_id) ON DELETE CASCADE,
    ticker TEXT NOT NULL,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, ticker)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_holdings_user_id ON holdings(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_watchlist_user_id ON watchlist(user_id);
```

### Step 3: Verify Tables Created
After executing the SQL, verify in Supabase:
- Go to **Table Editor** in the left sidebar
- You should see 5 tables: users, portfolios, holdings, transactions, watchlist

---

## Phase 1: Core Dashboard UI & Layout ✅
- [x] Design main dashboard layout with sidebar navigation, header, and content area
- [x] Create portfolio overview cards showing total value, day change, and available cash
- [x] Build stock holdings table with real-time prices and P&L tracking
- [x] Implement leaderboard section showing top performers by portfolio growth
- [x] Add responsive navigation between Dashboard, Trade, Portfolio, and Leaderboard pages

---

## Phase 2: Stock Search & Trading System ✅
- [x] Integrate Yahoo Finance API for NSE/BSE stock data and real-time prices
- [x] Build stock search interface with autocomplete for Indian stocks
- [x] Create detailed stock info cards with price charts, fundamentals, and key metrics
- [x] Implement buy/sell order form with quantity validation and preview
- [x] Add transaction history with date, type, quantity, price, and total cost
- [x] Calculate and update portfolio value automatically after each trade

---

## Phase 3: Advanced Analytics & User Features ✅
- [x] Build portfolio performance charts (line graph for value over time)
- [x] Add sector allocation pie chart and stock weightage visualization
- [x] Create user profile system with portfolio statistics and trading history
- [x] Implement global leaderboard with ranking, returns %, and badges
- [x] Add market watchlist for tracking favorite stocks without buying
- [x] Display complete Portfolio page with all analytics and visualizations

---

## Phase 4: Google OAuth Authentication & Login System ✅
- [x] Create login page with Google Sign-In button as entry point
- [x] Integrate reflex-google-auth for OAuth 2.0 authentication flow
- [x] Set up authentication state with user session management and Supabase integration
- [x] Add protected route middleware to require login for all dashboard pages
- [x] Display user profile info (name, email, avatar) in header with logout button
- [x] On first login, create new user in Supabase with ₹1,00,000 starting cash
- [x] Implement on_load check to validate token and restore user session

---

## Phase 5: User Data Persistence & Portfolio Loading
- [ ] Load user portfolio data from Supabase on authentication (cash, holdings, transactions)
- [ ] Load user watchlist from Supabase and sync with TradeState
- [ ] Update DashboardState.holdings from Supabase holdings table on page load
- [ ] Update TradeState.transactions from Supabase transactions table on page load
- [ ] Calculate portfolio_value and day_change from loaded holdings data
- [ ] Display user-specific data instead of mock data

---

## Phase 6: Real-time Database Sync for Trading Operations
- [ ] Update buy_stock event to persist purchases to Supabase holdings table
- [ ] Update buy_stock event to record transaction in Supabase transactions table
- [ ] Update buy_stock event to update portfolios.available_cash in Supabase
- [ ] Update sell_stock event to update/delete holdings in Supabase
- [ ] Update sell_stock event to record sell transaction in Supabase
- [ ] Implement remove stock functionality (sell entire position) with database sync
- [ ] Update toggle_watchlist to persist changes to Supabase watchlist table
- [ ] Sync portfolio.total_value to Supabase after every trade

---

## Technical Stack
- Authentication: reflex-google-auth with OAuth 2.0
- Database: Supabase (PostgreSQL) for persistent storage
- Backend: Reflex State Management with async database operations
- Data: Yahoo Finance API (yfinance library) for real-time stock prices
- UI: Modern SaaS design with purple accent
- Charts: Recharts via Reflex

---

## Current Status
- Phases 1-4: ✅ Complete (UI, trading, and authentication)
- Phase 5: 🔄 In Progress (Loading user data from database)
- Phase 6: ⏳ Pending (Syncing trades to database)

---

## 📝 Important Notes

1. **Database Setup**: Execute the SQL above in Supabase before testing login
2. **Environment Variables**: Ensure GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SUPABASE_URL, SUPABASE_KEY are set
3. **First Login**: New users automatically get ₹1,00,000 starting balance
4. **Data Isolation**: Each user sees only their own portfolio data