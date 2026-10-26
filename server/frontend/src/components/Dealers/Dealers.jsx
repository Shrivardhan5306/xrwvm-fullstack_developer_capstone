import React, { useState, useEffect } from "react";
import Header from "../Header/Header";
import "./Dealers.css";
import { Link } from "react-router-dom";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);
  const [state, setState] = useState("All");
  const [username] = useState(sessionStorage.getItem("username") || "");

  const curr_url = window.location.href;
  const root_url = curr_url.substring(0, curr_url.indexOf("dealers"));
  const all_dealers_url = root_url + "djangoapp/get_dealers";
  const dealers_by_state_url = root_url + "djangoapp/get_dealers/";

  const filterDealers = async (state) => {
    setState(state);
    let url = state === "All" ? all_dealers_url : dealers_by_state_url + state;
    const res = await fetch(url);
    const retobj = await res.json();
    if (retobj.status === 200) {
      let all_dealers = Array.from(retobj.dealers);
      setDealersList(all_dealers);
    }
  };

  useEffect(() => {
    fetch(all_dealers_url)
      .then((res) => res.json())
      .then((retobj) => {
        if (retobj.status === 200) {
          let all_dealers = Array.from(retobj.dealers);
          let unique_states = [...new Set(all_dealers.map((d) => d.state))];
          setDealersList(all_dealers);
          setStates(["All", ...unique_states]);
        }
      });
  }, []);

  return (
    <div>
      <Header />
      <div>
        <label htmlFor="state-filter">Filter by State: </label>
        <select id="state-filter" onChange={(e) => filterDealers(e.target.value)}>
          {states.map((s, i) => (
            <option key={i} value={s}>{s}</option>
          ))}
        </select>
      </div>
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
            <th>State</th>
            <th>Review Dealer</th>
            {username && <th>Post Review</th>}
          </tr>
        </thead>
        <tbody>
          {dealersList.map((dealer) => (
            <tr key={dealer.id}>
              <td>{dealer.id}</td>
              <td>{dealer.full_name}</td>
              <td>{dealer.city}</td>
              <td>{dealer.address}</td>
              <td>{dealer.zip}</td>
              <td>{dealer.state}</td>
              <td><Link to={"/dealer/" + dealer.id}>Review Dealer</Link></td>
              {username && (
                <td><Link to={"/dealer/" + dealer.id + "/postreview"}>Post Review</Link></td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Dealers;
