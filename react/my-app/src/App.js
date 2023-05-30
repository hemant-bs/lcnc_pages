// Import React and necessary components
import React, { useState } from 'react';

// Create a functional component
function App() {
  // Define a state variable using the useState hook
  const [count, setCount] = useState(0);

  // Define a function to increment the count
  const incrementCount = () => {
    setCount(count + 1);
  };

  // Define a function to decrement the count
  const decrementCount = () => {
    setCount(count - 1);
  };

  // Render the component
  return (
    <><div>
      <h1>React Counter</h1>
      <p>Count: {count}</p>
      <button onClick={incrementCount} id='increment'>Increment</button>
      <button onClick={decrementCount} id='decrement'>Decrement</button>
    </div><div>
        <h1 data-test="component-title">Title</h1>
        <p data-testid="component-paragraph">This is a paragraph.</p>
        <ul>
          <li data-test-id="list-item">Item 1</li>
          <li data-ti="list-item">Item 2</li>
          <li data-cy="list-item">Item 3</li>
          <li data-qa="list-item">Item 4</li>
          <li data-automation="list-item">Item 5</li>
        </ul>
      </div></>
  );
}

// Export the component as default
export default App;

