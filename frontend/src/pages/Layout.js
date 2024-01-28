import { Outlet, Link } from "react-router-dom";

// TODO: build header/footer here

const Layout = () => {
  return (
    <>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/parse">Parse</Link>
          </li>
          <li>
            <Link to="/cuisine">Cuisine</Link>
          </li>
          <li>
            <Link to="/graph">Graph</Link>
          </li>
        </ul>
      </nav>

      <Outlet />
    </>
  );
};

export default Layout;
