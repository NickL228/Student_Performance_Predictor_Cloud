import { useState } from "react";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    study_hours: "",
    attendance: "",
    assignment_score: "",
    previous_grade: ""
  });

  const [authData, setAuthData] = useState({
    username: "",
    password: ""
  });

  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);
  const [users, setUsers] = useState([]);
  const [user, setUser] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const [authMessage, setAuthMessage] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleAuthChange = (e) => {
    setAuthData({ ...authData, [e.target.name]: e.target.value });
  };

  const registerUser = async () => {
    setAuthMessage("");
    setError("");

    try {
      const response = await fetch("/api/register/", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(authData)
      });

      const data = await response.json();

      if (response.ok) {
        setAuthMessage(data.message);
      } else {
        setAuthMessage(data.error);
      }
    } catch {
      setError("Network error");
    }
  };

  const loginUser = async () => {
    setAuthMessage("");
    setError("");

    try {
      const response = await fetch("/api/login/", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(authData)
      });

      const data = await response.json();

      if (response.ok) {
        setUser(data.username);
        setIsAdmin(data.is_staff);
        setAuthMessage(data.message);
      } else {
        setAuthMessage(data.error);
      }
    } catch {
      setError("Network error");
    }
  };

  const logoutUser = async () => {
    try {
      await fetch("/api/logout/", {
        method: "POST",
        credentials: "include"
      });
    } catch {}

    setUser("");
    setIsAdmin(false);
    setUsers([]);
    setHistory([]);
    setResult("");
    setAuthMessage("Logged out");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult("");
    setError("");

    try {
      const response = await fetch("/api/predict/", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data.result);
        loadHistory();
      } else {
        setError(data.error || "Something went wrong");
      }
    } catch {
      setError("Could not connect to backend API");
    }
  };

  const loadHistory = async () => {
    try {
      const response = await fetch("/api/history/", {
        credentials: "include"
      });

      const data = await response.json();

      if (response.ok) {
        setHistory(data);
      } else {
        setError(data.error || "Could not load history");
      }
    } catch {
      setError("Could not load history");
    }
  };

  const deleteItem = async (id) => {
    try {
      const response = await fetch(`/api/delete/${id}/`, {
        method: "POST",
        credentials: "include"
      });

      if (response.ok) {
        loadHistory();
      } else {
        setError("Delete failed");
      }
    } catch {
      setError("Delete failed");
    }
  };

  const loadUsers = async () => {
    try {
      const response = await fetch("/api/users/", {
        credentials: "include"
      });

      const data = await response.json();

      if (response.ok) {
        setUsers(data);
      } else {
        setError(data.error);
      }
    } catch {
      setError("Could not load users");
    }
  };

  const deleteUser = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/api/users/delete/${id}/`, {
        method: "POST",
        credentials: "include"
      });

      const data = await response.json();

      if (response.ok) {
        loadUsers();
      } else {
        setError(data.error);
      }
    } catch {
      setError("Could not delete user");
    }
  };

  return (
    <div className="App">
      <h1>Student Performance Predictor</h1>

      <div className="auth-box">
        <h2>User Authentication</h2>

        {!user && (
          <>
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={authData.username}
              onChange={handleAuthChange}
            />

            <input
              type="password"
              name="password"
              placeholder="Password"
              value={authData.password}
              onChange={handleAuthChange}
            />

            <button type="button" onClick={registerUser}>Register</button>
            <button type="button" onClick={loginUser}>Login</button>
          </>
        )}

        {user && (
          <>
            <p>Logged in as: {user}</p>
            <button type="button" onClick={logoutUser}>Logout</button>
          </>
        )}

        {authMessage && <p>{authMessage}</p>}
      </div>

      {!user && (
        <p>Please register or log in to use the prediction system.</p>
      )}

      {user && (
        <>
          {isAdmin && (
            <div className="history">
              <button type="button" onClick={loadUsers}>Load Users</button>

              {users.length > 0 && (
                <>
                  <h2>Registered Users</h2>

                  <table>
                    <thead>
                      <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Admin</th>
                        <th>Action</th>
                      </tr>
                    </thead>

                    <tbody>
                      {users.map((item) => (
                        <tr key={item.id}>
                          <td>{item.id}</td>
                          <td>{item.username}</td>
                          <td>{item.is_staff ? "Yes" : "No"}</td>
                          <td>
                            {!item.is_staff && (
                              <button type="button" onClick={() => deleteUser(item.id)}>
                                Delete
                              </button>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </>
              )}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div>
              <label>Study Hours</label>
              <input
                type="number"
                name="study_hours"
                min="0"
                max="12"
                value={formData.study_hours}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label>Attendance (%)</label>
              <input
                type="number"
                name="attendance"
                min="0"
                max="100"
                value={formData.attendance}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label>Assignment Score</label>
              <input
                type="number"
                name="assignment_score"
                min="0"
                max="100"
                value={formData.assignment_score}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label>Previous Grade</label>
              <input
                type="number"
                name="previous_grade"
                min="0"
                max="100"
                value={formData.previous_grade}
                onChange={handleChange}
                required
              />
            </div>

            <button type="submit">Predict</button>
            <button type="button" onClick={loadHistory}>Load History</button>
          </form>

          {result && <h2>Prediction: {result}</h2>}

          {history.length > 0 && (
            <div className="history">
              <h2>Prediction History</h2>

              <table>
                <thead>
                  <tr>
                    <th>Study Hours</th>
                    <th>Attendance</th>
                    <th>Assignment</th>
                    <th>Previous Grade</th>
                    <th>Result</th>
                    <th>Date</th>
                    <th>Action</th>
                  </tr>
                </thead>

                <tbody>
                  {history.map((item) => (
                    <tr key={item.id}>
                      <td>{item.study_hours}</td>
                      <td>{item.attendance}</td>
                      <td>{item.assignment_score}</td>
                      <td>{item.previous_grade}</td>
                      <td>{item.result}</td>
                      <td>{item.created_at}</td>
                      <td>
                        <button type="button" onClick={() => deleteItem(item.id)}>
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default App;