import { Component, OnInit } from '@angular/core';
import { Global } from "../global";

@Component({
    selector: 'home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

    constructor() { }

    ngOnInit() {
    }
    origin = "";
    destination = "";
    train = "Train"
    submit() {
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
