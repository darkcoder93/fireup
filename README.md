# 🔥 FIRE Calculator

A comprehensive Django web application for calculating and tracking your Financial Independence, Retire Early (FIRE) number with support for both USA and Indian contexts.

## Features

### 🎯 Core FIRE Calculations
- **FIRE Number Calculator**: Calculate your target retirement amount using the 4% rule (or custom withdrawal rate)
- **Years to FIRE**: Estimate how long until you reach financial independence
- **Progress Tracking**: Visual progress bars and percentage completion
- **Multi-Country Support**: USA and India with different inflation and return rate defaults

### 📊 Monthly Tracking
- Track monthly income, expenses, and net worth
- Automatic savings rate calculation
- Historical data visualization
- Notes and annotations for each month

### 🎯 Goal Management
- Set financial goals (Emergency Fund, Debt Free, FIRE Number, etc.)
- Progress tracking with visual indicators
- Goal completion status
- Target dates and milestones

### 📈 Analytics & Insights
- Net worth growth charts
- Savings rate trends
- Income vs expenses analysis
- FIRE progress over time

### 🌍 Country-Specific Features
- **USA Context**: 2.5% inflation, 7% return rate, USD currency
- **India Context**: 6% inflation, 12% return rate, INR currency
- Automatic currency symbol display
- Country-specific default values

## Technology Stack

- **Backend**: Django 5.0+
- **Frontend**: Tailwind CSS (CDN)
- **Charts**: Chart.js
- **Database**: SQLite (default), supports PostgreSQL/MySQL
- **Package Manager**: uv (recommended)

## Installation & Setup

### Prerequisites
- Python 3.8+
- uv (recommended) or pip

### 1. Clone and Setup
```bash
cd finance_planning_tracking/fire_calculator
uv sync  # Install dependencies
```

### 2. Database Setup
```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### 3. Create Superuser (Optional)
```bash
uv run python manage.py createsuperuser
```

### 4. Run Development Server
```bash
uv run python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## Usage Guide

### 1. Initial Setup
1. Visit the application and click "Login"
2. Create a new account or use the admin interface
3. Complete your profile setup with:
   - Country selection (USA/India)
   - Current age and target retirement age
   - Annual income and expenses
   - Current net worth
   - FIRE calculation parameters

### 2. Monthly Tracking
1. Navigate to "Monthly Tracking"
2. Add your monthly financial data:
   - Monthly income
   - Monthly expenses
   - Current net worth
   - Optional notes
3. View your tracking history and trends

### 3. Goal Setting
1. Go to "Goals" section
2. Create financial goals like:
   - Emergency Fund
   - Debt Free
   - FIRE Number
   - Coast FIRE
   - Custom goals
3. Track progress and update amounts regularly

### 4. Analytics
1. Visit "Analytics" to see:
   - Net worth growth charts
   - Savings rate trends
   - Income vs expenses analysis
   - FIRE progress visualization

## FIRE Calculation Methods

### Standard FIRE Number
```
FIRE Number = Annual Expenses × (100 ÷ Withdrawal Rate)
```

### Years to FIRE
The application uses compound interest calculations to estimate years needed:
- Considers current net worth
- Accounts for annual savings
- Uses expected return rate
- Factors in inflation

### Country-Specific Defaults

| Country | Inflation Rate | Return Rate | Currency |
|---------|---------------|-------------|----------|
| USA     | 2.5%          | 7.0%        | USD ($)  |
| India   | 6.0%          | 12.0%       | INR (₹)  |

## Project Structure

```
fire_calculator/
├── fire_calculator/          # Main Django project
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── fire_tracker/            # Main app
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── urls.py              # App URL patterns
│   └── admin.py             # Admin interface
├── templates/               # HTML templates
│   └── fire_tracker/
│       ├── base.html        # Base template
│       ├── dashboard.html   # Main dashboard
│       ├── setup_profile.html
│       ├── monthly_tracking.html
│       ├── goals.html
│       └── login.html
├── static/                  # Static files
│   ├── css/
│   └── js/
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## Database Models

### UserProfile
- User financial information
- FIRE calculation parameters
- Country context

### MonthlyTracking
- Monthly income, expenses, net worth
- Automatic savings rate calculation
- Notes and timestamps

### FireProgress
- Historical FIRE progress tracking
- Progress percentages over time

### Goal
- Financial goal management
- Progress tracking
- Completion status

### InflationData
- Historical inflation data
- Country-specific rates

## Customization

### Adding New Countries
1. Update `FIRE_SETTINGS` in `settings.py`
2. Add country choice in `UserProfile.COUNTRY_CHOICES`
3. Update currency symbols and default rates

### Custom FIRE Calculations
Modify the calculation methods in `UserProfile` model:
- `fire_number` property
- `years_to_fire` property
- `fire_progress_percentage` property

### Styling
The application uses Tailwind CSS. Customize by:
- Modifying classes in templates
- Adding custom CSS in `base.html`
- Updating color schemes and components

## Deployment

### Production Settings
1. Update `settings.py`:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use environment variables for `SECRET_KEY`
   - Set up proper database (PostgreSQL recommended)

2. Static Files:
   ```bash
   uv run python manage.py collectstatic
   ```

3. Database:
   ```bash
   uv run python manage.py migrate
   ```

### Environment Variables
Create a `.env` file:
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

## Roadmap

- [ ] Advanced FIRE scenarios (Coast FIRE, Barista FIRE)
- [ ] Investment portfolio tracking
- [ ] Tax optimization calculations
- [ ] Mobile app version
- [ ] API endpoints for third-party integrations
- [ ] Export functionality (PDF reports, CSV data)
- [ ] Social features (anonymous community sharing)
- [ ] Real-time inflation data integration
- [ ] Multiple currency support
- [ ] Advanced analytics and forecasting

---

**Happy FIRE journey! 🔥💰**
