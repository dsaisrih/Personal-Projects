# Expense Management System - Test Cases

## Test Summary

### Authentication & Login
- [x] User Registration
- [x] User Login
- [x] Logout functionality
- [x] Redirect to login after logout

### User Isolation
- [x] Each user sees only their own expenses
- [x] Balance is separate per user
- [x] Charts filtered by user

### Balance Management
- [x] Initial balance check (shows 0 if no balance set)
- [x] Add balance functionality
- [x] Balance deduction on expense addition
- [x] Balance refund on expense deletion
- [x] Balance adjustment on expense update

### Expense CRUD Operations
- [x] Add Expense (validates all fields, calculates balance)
- [x] Edit Expense (updates record and adjusts balance)
- [x] Delete Expense (removes record and refunds balance)
- [x] View Expenses (displays in table with proper columns)

### Data Integrity
- [x] User ID stored with each expense
- [x] Treeview displays: ID, User_ID, Date, Category, Payment Method, Description, Amount
- [x] Select row functionality works correctly (adjusted for user_id column)
- [x] Amount conversion to float for calculations

### Reports & Exports
- [x] Bar Chart (Monthly breakdown)
- [x] Pie Chart (By category)
- [x] PDF Export (All expenses + charts)
- [x] Excel Export (All expenses + charts)
- [x] Month-Year Summary (with 00 for full year)

### Error Handling
- [x] Validation for empty fields
- [x] Validation for numeric amounts
- [x] Confirmation dialogs for delete operations
- [x] Error messages for operations

### UI/UX
- [x] Header with username display
- [x] Logout button in header
- [x] Login window redesigned
- [x] Form properly aligned and organized
- [x] Balance card shows current balance
- [x] Success/Error messages displayed

## Database Structure

### users table
- id (auto-increment)
- username (unique)
- password

### expenses table
- id (auto-increment)
- user_id (foreign key → users.id)
- date
- category
- paid_through
- description
- amount

### balance table
- user_id (primary key, foreign key → users.id)
- amount

## Fixed Issues

1. ✓ select_row function updated to handle user_id column (now at index 1)
2. ✓ add_expense validates input and clears form after success
3. ✓ update_expense calculates balance difference and confirms selection
4. ✓ delete_expense refunds balance and asks confirmation
5. ✓ Logout function properly redirects to login
6. ✓ Login window properly structured for re-login after logout
7. ✓ Code structure fixed (main_app is now separate function)
8. ✓ All queries filtered by user_id for proper data isolation

## Status: READY FOR PRODUCTION ✓
