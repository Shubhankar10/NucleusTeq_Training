//working with Flask api
import express from "express";
import bodyParser from "body-parser";
import axios from "axios";

const app = express();
const port = 3000;

app.use(express.static("public"));
app.use(bodyParser.urlencoded({ extended: true }));

app.get("/", async (req, res) => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/api/items");
    console.log("GET DATA recieved");
    const result = response.data;
    // console.log(result);
    res.render("solution.ejs", { data: result });
  } catch (error) {
    console.error("Failed to make request:", error.message);
    res.render("solution.ejs", {
      error: error.message,
    });
  }
});
app.post("/", async (req, res) => {
  try {
    const newItemData = {
      SerialNumber: '2020',
      ItemName: 'Computer',
      Quantity: 1,
      Category: 'Electronics',
      BillNumber: '000',
      DateOfPurchase: '2022-04-19',
      Warranty: '10 year',
      AssignedTo: 'JOJO'
    };
    const response = await axios.post('http://127.0.0.1:5000/api/items', newItemData);
    
    const result = response.data;
    console.log("POST succesfull");
    console.log(result);
    res.render("solution.ejs", {data: result});
  } catch (error) {
    console.log("POST failed");
    console.error("Failed to make request:", error.message);
    res.render("solution.ejs", {error: "NO POST",
    });
  }
});


app.listen(port, () => {
  console.log(`Server running on port: ${port}`);
});




