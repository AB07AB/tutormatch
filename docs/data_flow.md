# TutorMatch Data Flow Diagram

```mermaid
graph TD
    A[User Interface] -->|Login Request| B[Firebase Auth]
    B -->|Authentication Result| A
    A -->|Profile Data| C[SQLite Database]
    C -->|Retrieved Data| A
    A -->|Filter Criteria| D[Filter Processor]
    D -->|Filtered Results| A
    A -->|Profile Updates| C
```

### Description
1. **Firebase Auth**: Handles user authentication
2. **SQLite Database**: Stores and retrieves teacher profile data
3. **Filter Processor**: Processes filtering criteria for teacher search
4. **User Interface**: Main interaction point for all data operations
