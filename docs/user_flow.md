# TutorMatch User Flow Diagram

```mermaid
graph TD
    A[Welcome Screen] -->|Login| B[Login Screen]
    A -->|Sign Up| C[SignUp Screen]
    B -->|Successful Login| D[Student Dashboard]
    C -->|Successful Registration| E[Edit Profile Screen]
    D -->|Select Teacher| F[Teacher Details Screen]
    E -->|Save Changes| D
    F -->|Back| D
    B -->|Back| A
    C -->|Back| A
    E -->|Back| B
```

### Description
1. **Welcome Screen**: Entry point with options to login or sign up
2. **Login Screen**: Handles user authentication
3. **SignUp Screen**: New user registration
4. **Student Dashboard**: Main interface showing available teachers
5. **Teacher Details Screen**: Detailed view of selected teacher's profile
6. **Edit Profile Screen**: Allows teachers to update their profile information
