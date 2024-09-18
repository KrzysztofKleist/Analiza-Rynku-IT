// const h1 = document.createElement("h1")
// h1.textContent = "Hello world"
// h1.className = "header"
// console.log(h1)

// const element = <h1 className="header">This is JSX</h1>
// console.log(element)

// const page = (
//   <div>
//     <h1 className="header">This is JSX</h1>
//     <p>This is a paragraph</p>
//   </div>
// );

const navbar = (
  <nav>
    <h1>Website Name</h1>
    <ul>
      <li>Pricing</li>
      <li>About</li>
      <li>Contact</li>
    </ul>
  </nav>
);

// JSX - JavaScript XML
ReactDOM.render(navbar, document.getElementById("root"));
