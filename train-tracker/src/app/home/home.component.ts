import { Component, OnInit } from '@angular/core';
import { Global } from "../global";
import { Router } from "@angular/router";
import { HttpClient } from "@angular/common/http";

@Component({
    selector: 'home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
    // train_options = ['1', '2', '3', '4', '5', '6', '7', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'L', 'M', 'N', 'Q', 'R', 'S', 'W', 'Z']
    train_options = [{'name': '1'}, {'name': '2'}, {'name': '3'}, {'name': '4'}, {'name': '5'}, {'name': '6'}, {'name': '7'}, {'name': 'A'}, {'name': 'B'}, {'name': 'C'}, {'name': 'D'}, {'name': 'E'}, {'name': 'F'}, {'name': 'G'}, {'name': 'H'}, {'name': 'J'}, {'name': 'L'}, {'name': 'M'}, {'name': 'N'}, {'name': 'Q'}, {'name': 'R'}, {'name': 'S'}, {'name': 'W'}, {'name': 'Z'}]
    constructor(private router: Router, private http:HttpClient) { }

    ngOnInit() {
        this.tokens = Global.tokens;
    }
    origin = "";
    destination = "";
    train = "Train"
    tokens = 0;
    submit() {
        // Basic form validation
        if(this.origin == "" || this.destination == "" || this.train == "Train") {
            alert("You must specify an origin, destination, and train");
            return;
        }
        if(this.tokens <= 0) {
            alert("You do not have sufficient tokens");
            return;
        }
        // If number is negative then downtown (S), else uptown (N)
        // Check if there are numbers in string
        const difference = Number(this.extractNumber(this.destination)) - Number(this.extractNumber(this.origin))
        let direction = "";
        if(difference < 0) {
            direction = "S";
        } else {
            direction = "N";
        }
        console.log(this.origin, this.destination);
        Global.origin = this.origin + direction;
        Global.destination = this.destination;
        Global.train = this.train;
        Global.tokens--;
        this.http.post("http://localhost:5000/station-line-info", {"feed_id": Global.line_feeds[Global.train], "station_id": Global.origin}).subscribe(
            data => {
                for(const i of Object.keys(data)) {
                    Global.data.push(data[i]);
                }
                this.router.navigate(["/status"]);
            }, error => {
                alert("Error processing data");
            }
        )
    }
    setTrain(name) {
        this.train = name;
        console.log(name);
    }
    extractNumber(str) {
        let out = ""
        for(const char of str) {
            if(!isNaN(char)) {
                out += char;
            }
        }
        return out;
    }
}
