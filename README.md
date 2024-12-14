# Project Title: simple- tasker Tasks

## **Project Name: PyExpress Integration**

This project is a hands-on exploration of fundamental backend development concepts, focusing on implementing core functionalities without relying on frameworks or traditional database systems. It comprises a Python-based storage engine, a minimalistic custom server, and an authentication system. Additionally, an Express.js application serves as a middleware to handle HTML requests and responses, showcasing the integration of diverse technologies.

## **Components Overview**

### **1. Python Storage Engine**
The storage engine uses CSV files as a lightweight alternative to databases, enabling basic data management operations.

#### **CsvStorage Class**
- **Purpose:** Mimics database functionalities through file-based operations.
- **Core Methods:**
  - `write_line`: Appends data to the file.
  - `get_columns`: Extracts specific column data from the file.
- **Advanced Methods:**
  - `filter`, `get_by`, `add`, `delete`, `multi_selections`, and `search`: Build on the core methods to provide advanced storage capabilities.

### **2. Python Server**
A custom HTTP server is implemented to handle requests and responses, offering a low-level approach to web server functionalities.

#### **RequestHandler Class**
- **Key Methods:**
  - `_set_headers`: Configures HTTP response headers.
  - `serve_html`: Serves HTML files, primarily used for testing API functionality during development.
  - `parse_request_data`: Parses JSON data from incoming requests.
  - `do_GET`: Handles GET requests.
  - `do_POST`: Handles POST requests.
- **Development Approach:** This server was intentionally developed without frameworks to gain a deeper understanding of HTTP communication. Tools like Postman were avoided during development to rely entirely on server-side debugging.

### **3. Authentication System**
This system provides session management and token-based user authentication, ensuring secure access control.

#### **Tokens Class**
- **Functions:**
  - `__init__`: Initializes a token object.
  - `create`: Generates new tokens.
  - `validate_id`: Verifies the user ID associated with a token.
  - `validate_exp`: Checks token expiration.
  - `validate_all`: Performs comprehensive validation of token attributes.

#### **Authentication Class**
- **Role:** Integrates with the Tokens class to manage user sessions.
- **Session Storage:** Utilizes the file-based storage engine to persist session data by converting token objects into dictionaries.

### **4. Models**
The project includes data models for managing users, tasks, and tokens.

#### **Base Class**
- **Attributes:**
  - `created`: Timestamp of creation.
  - `updated`: Timestamp of last modification.
  - `id`: Unique identifier.
- **Methods:**
  - `to_dict`: Converts the object to a serializable dictionary.
  - `to_save`: Prepares data for secure storage, such as hashing passwords.
  - `serializer`: Cleanses sensitive attributes to ensure safe serialization.

#### **Derived Classes**
- **Users:** Manages user-related data.
- **Tasks:** Handles task-specific operations.
- **Tokens:** Manages token-specific information.

### **5. Express.js Application**
The Express.js application acts as a middleware layer, facilitating communication between the user interface and the Python backend.

#### **Roles:**
1. **Request Proxying:** Forwards client requests to the Python server.
2. **HTML Serving:** Provides an interface for interacting with the API during development and testing.
3. **Technology Integration:** Demonstrates the interoperability of Express.js and a custom Python backend.

## **Project Philosophy**
- Emphasis on understanding core backend principles by minimizing reliance on external frameworks.
- Exploration of fundamental operations, such as HTTP request handling, file-based data storage, and session management.
- Integration of lightweight technologies for a cohesive development experience.

## **Key Features**
- A custom CSV-based storage engine with advanced query capabilities.
- A low-level Python server for handling HTTP requests and responses.
- A robust token-based authentication system.
- Flexible models for users, tasks, and tokens.
- An Express.js application for serving HTML and facilitating communication with the backend.

This project serves as a comprehensive learning experience, blending simplicity and functionality to build a solid foundation in backend development.
