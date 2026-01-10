---

# MiniCRM Feature Implementation: Signup & Profile

## Feature Choice & Rationale

The feature implemented is **Signup and User Profile Management**. This feature allows users to register, create a detailed profile, and manage their personal information within the context of a company. This feature was chosen to:

* Enable users to maintain personal and company-related information.
* Extend CRM capabilities to track users, their roles, and departments.
* Provide a foundation for viewing and interacting with user profiles across the system.

---

## Technical Approach & Design Decisions

### Backend (Django REST Framework)

1. **User Model Extension**

   * Created a `UserProfile` model linked to the default Django `User` model.
   * Added fields: `phone`, `job_title`, `department`, `company`, `profile_picture`, `bio`.
   * Automatically create/update user profile using `post_save` signal.

2. **API Endpoints**

   * **Signup:** Registers a user and creates an associated profile.
   * **Profile:** Retrieve and update profile information.
   * Validation ensures correct format and required fields.

3. **Error Handling & Validation**

   * Unique email enforcement.
   * Profile fields validation.
   * Descriptive error responses for invalid inputs.

### Frontend (Vue 3 + Vuetify)

1. **Components**

   * `RegisterView.vue`: User registration with profile information.
   * `ProfileView.vue`: Display and update user profile.

2. **Integration**

   * Routes added in `router/index.js`.
   * API calls handled through `services/api.js`.
   * Updates to `App.vue` for navigation to new views.

3. **User Experience Enhancements**

   * Graceful confirmation dialogs for deletion actions.
   * Client-side validation for required fields and address format.
   * Loading indicators and error messages for network actions.

### Design Decisions

* Separation of concerns between frontend and backend.
* Modular and reusable components.
* Ensured relational integrity between users and companies.
* Scalable architecture for future profile-related features.

---

## Implementation Details

**Backend Files:**

* `models.py`: Added `UserProfile` model.
* `serializers.py`: Added `UserProfileSerializer`.
* `views.py`: Added `SignupView` and `ProfileView`.
* `urls.py`: Added `/auth/signup/` and `/auth/profile/` endpoints.
* `migrations/0003_userprofile.py`: Migration for `UserProfile`.

**Frontend Files:**

* `ProfileView.vue` and `RegisterView.vue`: Forms for registration and profile management.
* `App.vue`: Updated navigation links.
* `router/index.js`: Added routes for register and profile pages.
* `services/api.js`: Added functions for signup and fetching/updating profile.
* Existing views (`CompaniesView.vue`, `ContactsView.vue`, `DealsView.vue`, `LoginView.vue`, `TasksView.vue`): Replaced default browser alerts with Vuetify dialogs and refined deletion logic.

**UX/UI Improvements:**

* Required fields clearly marked.
* Client-side validation for address and input formats.
* Feedback for invalid or incomplete submissions.

---

## Testing

**Test Cases (5+):**

1. **Positive:** Successful user signup with valid inputs.
2. **Negative:** Signup fails when required fields are missing.
3. **Positive:** Profile updates successfully with valid data.
4. **Negative:** Profile update fails with invalid phone or email.
5. **Edge Case:** User attempts to delete company or profile; proper confirmation dialog appears.

* Mocked API responses for signup and profile retrieval.
* Validated that migrations work on a fresh database.

---

## Challenges & Trade-offs

* Ensuring profile creation on signup required careful use of signals.
* UI consistency required adjustments in existing views to maintain styling and interactions.
* Trade-off: Full user-to-user profile view not implemented due to time constraints but scaffolded for future development.

---

## Setup & Testing Instructions

1. **Clone Repository**

```bash
git clone <repo-url>
cd UnityMiniCRM
```

2. **Setup Backend**

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate
pip install -r backend/requirements.txt
python manage.py migrate
python manage.py runserver
```

3. **Setup Frontend**

```bash
cd frontend
npm install
npm run serve
```

4. **Test Feature**

* Navigate to `/register` to create a new user.
* Access `/profile` to view and update profile.
* Verify deletion dialogs and client-side validation.

5. **Run Automated Tests**

From the project backend folder, create/activate your virtual environment, install dependencies, then run the Django test suite:

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt
python manage.py test
```

To run only the `tasks` app tests:

```bash
python manage.py test tasks
```

---

## Future Improvements

* Implement user-to-user profile view.
* Add profile picture upload and cropping.
* Allow company administrators to manage users.
* Enhance form validation with more complex rules.
* Add automated tests for all CRUD operations.

---

## Database Migrations

* `0003_userprofile.py`: Added `UserProfile` model.
* Ensure migration runs successfully on a fresh database.

---

*End of Solution*
