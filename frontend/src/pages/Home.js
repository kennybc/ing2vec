import React, { useEffect, useState } from "react";

function htmlDecode(input) {
  var e = document.createElement("textarea");
  e.innerHTML = input;
  // handle case of empty input
  return e.childNodes.length === 0 ? "" : e.childNodes[0].nodeValue;
}

const Home = () => {
  const [recipe, setRecipe] = useState({});

  // useeffect so it only fetches once
  // remove if want to continuously fetch latest every time new recipe is crawled
  useEffect(() => {
    fetch("/recipe/latest")
      .then((response) => response.json())
      .then((data) => setRecipe(data));

    /*const source = new EventSource("http://localhost:5000/recipe/current");

        source.onmessage = () => {
          console.log("update");
        }*/
  }, []);

  if (!recipe || recipe === undefined || recipe.name == undefined) {
    return <h1> Loading... </h1>;
  }
  return (
    <div>
      <h1> {htmlDecode(recipe.name)} </h1>
      <h2> Ingredients </h2>
      <ul>
        {recipe.ingredients.map((item, index) => {
          return <li key={index}> {item} </li>;
        })}
      </ul>
      <h2> NER </h2>
      <ul>
        {recipe.ner.map((item, index) => {
          return <li key={index}> {item} </li>;
        })}
      </ul>
    </div>
  );
};

export default Home;
