import React, { useEffect, useState } from "react";
import "./App.css";

function htmlDecode(input) {
    var e = document.createElement("textarea");
    e.innerHTML = input;
    // handle case of empty input
    return e.childNodes.length === 0 ? "" : e.childNodes[0].nodeValue;
}

function App() {
    const [recipe, setRecipe] = useState({});
    const [ingredients, setIngredients] = useState([]);

    useEffect(() => {
        fetch("/recipe/latest")
            .then((response) => response.json())
            .then((data) => {
                setRecipe(data);
                data.ingredients.map((item, index) => {
                    fetch("/parse/" + encodeURI(item))
                        .then((response) => response.json())
                        .then((parsed) =>
                            setIngredients((arr) => [
                                ...arr,
                                <li key={index}>
                                    {item} ...... {parsed}
                                </li>,
                            ])
                        );
                });
            });

        /*const source = new EventSource("http://localhost:5000/recipe/current");

        source.onmessage = () => {
          console.log("update");
        }*/
    }, []);

    if (
        !recipe ||
        recipe === undefined ||
        recipe === {} ||
        !recipe.ingredients
    ) {
        return <h1> Loading... </h1>;
    }
    return (
        <div>
            <h1> {htmlDecode(recipe.name)} </h1>
            {recipe.ingredients.map((item, index) => {
                return (
                    <li key={index}>
                        {item} ...... {ingredients[index]}
                    </li>
                );
            })}
        </div>
    );
}

export default App;
