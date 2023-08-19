import React, { useEffect, useState } from 'react';
import './App.css';

const apiUri = process.env.REACT_APP_API_BASE_URL;

function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');
  const [reloadTodos, setReloadTodos] = useState(0);

  useEffect(() => {
    fetch(apiUri)
      .then(response => response.json())
      .then(data => {
        const remappedTodos = data.map(todo => ({
          id: todo[0],
          todo: todo[1],
          date: todo[2],
          time: todo[3],
          status: todo[4],
          isEditing: false // Add the isEditing flag
        }));

        setTodos(remappedTodos);
      })
      .catch(error => {
        console.error('Error fetching todos:', error);
      });
  }, [reloadTodos]);

  const handleEditToggle = (id) => {
    setTodos(prevTodos =>
      prevTodos.map(todo =>
        todo.id === id ? { ...todo, isEditing: !todo.isEditing } : todo
      )
    );
  };

  const handleEditChange = (id, newValue) => {
    setTodos(prevTodos =>
      prevTodos.map(todo =>
        todo.id === id ? { ...todo, todo: newValue } : todo
      )
    );
  };

  const handleEditSave = async (id) => {
    const todoToUpdate = todos.find(todo => todo.id === id);
    if (!todoToUpdate) return;

    try {
      const response = await fetch(`${apiUri}/edit/${id}/${todoToUpdate.todo}`, {
        method: 'GET',
      });

      if (response.ok) {
        handleEditToggle(id);
      } else {
        console.error('Error updating todo:', response.statusText);
      }
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  }

  const handleToggleStatus = async (id, newStatus) => {
    try {
      const response = await fetch(`${apiUri}/${newStatus}/${id}`, {
        method: 'GET',
      });

      if (response.ok) {
        setTodos(prevTodos =>
          prevTodos.map(todo =>
            todo.id === id ? { ...todo, status: newStatus === 'check' ? 'True' : 'False' } : todo
          )
        );
      } else {
        console.error('Error toggling status:', response.statusText);
      }
    } catch (error) {
      console.error('Error toggling status:', error);
    }
  };

  const handleAddTodo = async () => {
    if (!newTodo) return;

    try {
      const response = await fetch(`${apiUri}/add/${newTodo}`, {
        method: 'GET',
      });

      if (response.ok) {
        setReloadTodos(reloadTodos + 1);
        setNewTodo('');
      } else {
        console.error('Error adding todo:', response.statusText);
      }
    } catch (error) {
      console.error('Error adding todo:', error);
    }
  };

  const handleDeleteTodo = async (id) => {
    try {
      const response = await fetch(`${apiUri}/delete/${id}`, {
        method: 'GET',
      });

      if (response.ok) {
        setReloadTodos(reloadTodos + 1);
      } else {
        console.error('Error deleting todo:', response.statusText);
      }
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  };

  return (
    <div className="App">
      <h1>Todos</h1>
      <div className="add-todo">
        <input
          type="text"
          value={newTodo}
          onChange={e => setNewTodo(e.target.value)}
          placeholder="Add a new todo..."
        />
        <button onClick={handleAddTodo}>Add</button>
      </div>
      <ul>
      {todos.map(todo => (
        <li key={todo.id}>
          <div>
            <strong>Todo:</strong> 
            {todo.isEditing ? (
              <input
                type="text"
                value={todo.todo}
                onChange={e => handleEditChange(todo.id, e.target.value)}
                autoFocus
              />
            ) : (
              <span> {todo.todo}</span>            
            )}
          </div>
          <div>
            <strong>Date:</strong> {todo.date}
          </div>
          <div>
            <strong>Time:</strong> {todo.time}
          </div>
          <div>
            <label>
              <input
                type="checkbox"
                checked={todo.status === 'True'}
                onChange={() =>
                  handleToggleStatus(todo.id, todo.status === 'True' ? 'uncheck' : 'check')
                }
              />
              Done
            </label>
          </div>
          <div>
            {todo.isEditing ? (
              <button onClick={() => handleEditSave(todo.id, todo.todo)}>Save</button>
            ) : (
              <button onClick={() => handleEditToggle(todo.id)}>Edit</button>
            )}
            <button onClick={() => handleDeleteTodo(todo.id)}>Delete</button>
          </div>
        </li>
      ))}
    </ul>
    </div>
  );
}

export default App;
