import React, { useState, useEffect } from "react";
import Header from "../Header/Header";
import { useParams } from "react-router-dom";

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);
  const [purchase, setPurchase] = useState(false);

  const curr_url = window.location.href;
  const root_url = curr_url.substring(0, curr_url.indexOf("postreview"));
  const { id } = useParams();
  const dealer_url = root_url + "djangoapp/dealer/" + id;
  const review_url = root_url + "djangoapp/add_review";
  const carmodels_url = root_url + "djangoapp/get_cars";

  useEffect(() => {
    fetch(dealer_url)
      .then((res) => res.json())
      .then((data) => setDealer(data.dealer));
    fetch(carmodels_url)
      .then((res) => res.json())
      .then((data) => setCarmodels(data.CarModels));
  }, []);

  const postreview = async () => {
    let name = sessionStorage.getItem("firstname") + " " + sessionStorage.getItem("lastname");
    let reviewobj = {
      name: name,
      dealership: id,
      review: review,
      purchase: purchase,
      purchase_date: date,
      car_make: model.split(" ")[0],
      car_model: model.split(" ").slice(1).join(" "),
      car_year: year,
    };
    const res = await fetch(review_url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(reviewobj),
    });
    const json = await res.json();
    if (json.status === 200) {
      window.location.href = window.location.origin + "/dealer/" + id;
    }
  };

  return (
    <div>
      <Header />
      <h1 style={{ paddingLeft: "5%" }}>Post a Review for {dealer.full_name}</h1>
      <div id="postreview_form">
        <textarea
          id="review"
          cols="70"
          rows="7"
          placeholder="Write your review..."
          onChange={(e) => setReview(e.target.value)}
        ></textarea>
        <div>
          <input
            type="checkbox"
            id="purchase"
            onChange={(e) => setPurchase(e.target.checked)}
          />
          <label htmlFor="purchase"> Did you purchase this vehicle? </label>
        </div>
        {purchase && (
          <div>
            <select onChange={(e) => setModel(e.target.value)}>
              <option value="" disabled selected>Select Car Make and Model</option>
              {carmodels.map((car, index) => (
                <option key={index} value={`${car.CarMake} ${car.CarModel}`}>
                  {car.CarMake} {car.CarModel}
                </option>
              ))}
            </select>
            <input
              type="number"
              placeholder="Car Year"
              onChange={(e) => setYear(e.target.value)}
            />
            <input
              type="date"
              placeholder="Purchase Date"
              onChange={(e) => setDate(e.target.value)}
            />
          </div>
        )}
        <div>
          <button id="post_review" onClick={postreview}>Post Review</button>
        </div>
      </div>
    </div>
  );
};

export default PostReview;
