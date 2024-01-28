import React, { useState } from "react";

export default function Cuisine() {
  const [cuisine, setCuisine] = useState("");
  const [recipes, setRecipes] = useState({});

  const fetchCuisine = (e) => {
    e.preventDefault();
    fetchApi("/cuisine/" + encodeURIComponent(cuisine));
  };

  const fetchApi = (api) => {
    fetch(api)
      .then((response) => response.json())
      .then((data) => {
        setRecipes(data);
      });
  };

  return (
    <div>
      <h1>Cuisine</h1>
      <h2> Search Cuisine </h2>
      <form onSubmit={fetchCuisine}>
        <input
          id="phrase"
          type="text"
          placeholder="Asian"
          onChange={(e) => setCuisine(e.target.value)}
        />
        <button type="submit"> Search </button>
      </form>
      {!Object.keys(recipes).length ? (
        <div>
          <h2> Waiting... </h2>
        </div>
      ) : (
        <div>
          <h2> Results </h2>
          <ul>
            {recipes.data.map((item, index) => {
              return <li key={index}> {item.name} </li>;
            })}
          </ul>
          {"prev_page" in recipes.pagination && (
            <button
              onClick={() => {
                fetchApi(recipes.pagination.prev_page);
              }}
            >
              Previous Page
            </button>
          )}
          {"next_page" in recipes.pagination && (
            <button
              onClick={() => {
                fetchApi(recipes.pagination.next_page);
              }}
            >
              Next Page
            </button>
          )}
        </div>
      )}
    </div>
  );
}
