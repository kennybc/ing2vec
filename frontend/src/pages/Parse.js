import React, { useEffect, useState } from "react";

const Parse = () => {
  const [phrase, setPhrase] = useState("");
  const [parsed, setParsed] = useState({});

  const parseIngredients = (e) => {
    e.preventDefault();
    fetch("/infer/" + encodeURIComponent(phrase))
      .then((response) => response.json())
      .then((data) => {
        setParsed(data);
      });
  };

  return (
    <div>
      <h1>Parse</h1>
      <h2> Ingredient Phrase </h2>
      <form onSubmit={parseIngredients}>
        <input
          id="phrase"
          type="text"
          placeholder="2 cups flour"
          onChange={(e) => setPhrase(e.target.value)}
        />
        <button type="submit"> Parse </button>
      </form>
      {!Object.keys(parsed).length ? (
        <div>
          <h2> Waiting... </h2>
        </div>
      ) : (
        <div>
          <h2> Results </h2>
          <ul>
            {parsed.ingredients.map((item, index) => {
              return <li key={index}> {item} </li>;
            })}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Parse;
