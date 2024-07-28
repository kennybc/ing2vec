import cytoscape from "cytoscape";
import popper from "cytoscape-popper";
import { useEffect, useState } from "react";
import fcose from "cytoscape-fcose";

import "./graph.css";

cytoscape.use(fcose);
cytoscape.use(popper);

export default function Graph() {
  const [ready, setReady] = useState(false);
  const [nodesReady, setNodesReady] = useState(false);
  const [edgesReady, setEdgesReady] = useState(false);
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  const fetchNodes = (api) => {
    return fetch(api)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        let structured = data.data.map((node) => {
          return {
            data: {
              id: node["_id"],
              label: node.name,
              weight: node.count,
            },
          };
        });
        setNodes((prevNodes) => {
          return prevNodes.concat(structured);
        });
        if ("next_page" in data.pagination) {
          return fetchNodes(data.pagination.next_page);
        }
      });
  };
  // TODO: first, load nodes/edges into unformatted table
  // then, format into cytoscape data
  // necessary for calcing PMI
  const fetchEdges = (api) => {
    return fetch(api)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        let structured = data.data.map((edge) => {
          return {
            data: {
              id: edge["_id"],
              //label: node.count,
              source: edge.node1,
              target: edge.node2,
              weight: edge.count,
            },
          };
        });
        setEdges((prevEdges) => {
          return prevEdges.concat(structured);
        });
        if ("next_page" in data.pagination) {
          return fetchEdges(data.pagination.next_page);
        }
      });
  };
  // TODO: wait for fetch to finish before adding to cytoscape
  // TODO: restructure mongodb to have ids as source/target instead of names
  useEffect(() => {
    fetchNodes("/nodes").then(() => {
      setNodesReady(true);
    });
    fetchEdges("/edges").then(() => {
      setEdgesReady(true);
    });
  }, []);

  useEffect(() => {
    if (nodesReady && edgesReady) {
      setReady(true);
    }
  }, [nodesReady, edgesReady]);

  useEffect(() => {
    const elements = nodes.concat(edges);
    const cy = cytoscape({
      container: document.getElementById("cy"),
      quality: "proof",
      randomize: false,
      style: [
        // the stylesheet for the graph
        {
          selector: "node",
          style: {
            "background-color": "#666",
            width: "mapData(weight, 0, 50, 5, 50)",
            height: "mapData(weight, 0, 50, 5, 50)",
          },
        },

        {
          selector: "edge",
          style: {
            "line-color": "#777",
            "curve-style": "bezier",
            width: "mapData(weight, 0, 20, 1, 3)",
            opacity: "mapData(weight, 0, 20, 0.2, 1)",
          },
        },
      ],

      layout: {
        name: "fcose",
      },

      elements: elements,
    });
    cy.nodes().unbind("mouseover");
    cy.nodes().bind("mouseover", (event) => {
      let popper = event.target.popper({
        content: () => {
          let content = document.createElement("div");
          content.classList.add("popper-div");
          content.innerHTML = event.target.data().label;
          document.body.appendChild(content);
          return content;
        },
      });
      event.target.popperRefObj = popper;
      let update = () => {
        popper.update();
      };
      event.target.on("position", update);
      cy.on("pan zoom resize", update);
    });

    cy.nodes().unbind("mouseout");
    cy.nodes().bind("mouseout", (event) => {
      if (event.target.popper) {
        event.target.popperRefObj.state.elements.popper.remove();
        event.target.popperRefObj.destroy();
      }
    });
  }, [ready]);

  return (
    <div
      style={{ height: "600px", width: "1000px", background: "#eee" }}
      id="cy"
    ></div>
  );
}
