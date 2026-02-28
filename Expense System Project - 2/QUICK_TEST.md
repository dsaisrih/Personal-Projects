# Quick Test Guide - Expense Management System

## 🚀 How to Run
```
python expense.py
```

## 👤 Test Users (Create These)
- Username: `john` Password: `pass123`
- Username: `sarah` Password: `pass456`

## 🧪 Quick Test Sequence

### 1️⃣ First Time Setup
```
1. Click "Register"
2. Enter username: "testuser"
3. Enter password: "test123"
4. Click "Register" → Success message
5. Click "Login"
6. Enter same credentials → Should enter main app
```

### 2️⃣ Balance Management
```
1. See "Current Balance : ₹ 0.00"
2. Type "5000" in Add Amount field
3. Click "✓ Add Balance"
4. Verify balance shows "₹ 5,000.00"
```

### 3️⃣ Add Expense
```
1. Click "📅 Pick" to select date (or type 2024-01-15)
2. Select Category: "Food"
3. Select Paid Through: "Cash"
4. Type Description: "Lunch"
5. Type Amount: "500"
6. Click "✓ Add"
7. Verify: Balance changes to ₹ 4,500.00
8. Expense appears in table
```

### 4️⃣ Edit Expense
```
1. Click on expense in table to select
2. Fields populate automatically
3. Change amount from 500 to 750
4. Click "✎ Update"
5. Verify: Balance changes to ₹ 4,250.00
```

### 5️⃣ Delete Expense
```
1. Click on expense to select
2. Click "✕ Delete"
3. Click "Yes" in confirmation
4. Verify: Expense removed, balance refunded
```

### 6️⃣ Charts
```
1. Click "📊 Bar Chart" → Monthly breakdown chart opens
2. Click "🥧 Pie Chart" → Category breakdown chart opens
```

### 7️⃣ Exports
```
1. Click "📄 PDF (All)" → Creates PDF with all expenses + charts
2. Click "📊 Excel (All)" → Creates Excel with all expenses + charts
3. Files save in PDF/ and EXCEL/ folders
```

### 8️⃣ Monthly Report
```
1. Type Month: "01" (for full year: "00")
2. Type Year: "2024"
3. Click "📅 Generate Report"
4. Creates PDF and Excel with filtered data + charts
```

### 9️⃣ Logout & Re-login
```
1. Click "🚪 Logout" in top right
2. Click "Yes" in confirmation
3. Redirected to login screen
4. Login with different user
5. See different expenses (data isolation)
```

## ✅ Verification Checklist

- [ ] Balance updates correctly on add/edit/delete
- [ ] Expenses show in table with correct info
- [ ] Select row populates form fields correctly
- [ ] Charts generate without errors
- [ ] PDF/Excel exports contain charts
- [ ] Each user only sees their own data
- [ ] Logout works and redirects to login
- [ ] Re-login works with clean user context
- [ ] All buttons disabled if no selection needed
- [ ] Error messages appear for invalid input

## 🔍 Common Issues & Solutions

**Issue: Balance shows 0 after adding expense**
- Solution: Ensure balance was added before expense

**Issue: Editing causes data loss**
- Solution: Select the row first (click in table)

**Issue: Can't logout**
- Solution: Click button labeled "🚪 Logout" in top right header

**Issue: Charts don't show**
- Solution: Add multiple expenses with different dates/categories

**Issue: Different users see same data**
- Solution: Logout completely and login with new user account
