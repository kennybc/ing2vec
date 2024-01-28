import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./pages/Layout.js";
import Home from "./pages/Home.js";
import Parse from "./pages/Parse.js";
import Cuisine from "./pages/Cuisine.js";
import Graph from "./pages/Graph.js";
import NotFound from "./pages/NotFound.js";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="parse" element={<Parse />} />
          <Route path="cuisine" element={<Cuisine />} />
          <Route path="graph" element={<Graph />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
