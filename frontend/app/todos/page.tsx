import React from 'react';

type Todo = {
  id: string;
  task: string;
  is_complete: boolean;
  created_at: string;
};

async function getTodos() {
  // Fetching from localhost backend
  try {
      const res = await fetch('http://127.0.0.1:8000/todos', { cache: 'no-store' });
      if (!res.ok) {
        throw new Error('Failed to fetch data');
      }
      return res.json();
  } catch (error) {
      console.error("Error fetching todos:", error);
      return [];
  }
}

export default async function TodosPage() {
  const todos: Todo[] = await getTodos();

  return (
    <div className="p-8 font-sans max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center">Todo List</h1>
      <ul className="space-y-3">
        {todos.length === 0 ? (
            <li className="text-center text-gray-500">No todos found or backend unavailable.</li>
        ) : (
            todos.map((todo) => (
            <li key={todo.id} className="p-4 border rounded-lg shadow-sm bg-white flex items-center gap-3 transition hover:shadow-md">
                <span className={`flex items-center justify-center w-6 h-6 rounded-full border ${todo.is_complete ? "bg-green-100 border-green-500 text-green-600" : "border-gray-300 text-transparent"}`}>
                ✓
                </span>
                <span className={todo.is_complete ? "line-through text-gray-400" : "text-gray-800 font-medium"}>
                {todo.task}
                </span>
            </li>
            ))
        )}
      </ul>
    </div>
  );
}
