import { Component, OnInit } from '@angular/core';
import { Global } from "../global";
import { HttpClient } from '@angular/common/http';
import { Router } from "@angular/router";

@Component({
    selector: 'app-status',
    templateUrl: './status.component.html',
    styleUrls: ['./status.component.css']
})
export class StatusComponent implements OnInit {
    
    data = [];
    constructor(private http: HttpClient, private router: Router) { }
    tokens = 0;

    ngOnInit() {
        this.tokens = Global.tokens;
        console.log("Sending feed id:", Global.line_feeds[Global.train]);
        console.log("Sending station id:", Global.origin);
        // Initialize data with objects of keys: predicted, scheculed, and difference
        this.data = Global.data.slice(0);
    }
    test() {
        console.log("Hello world");
    }
    modalStatus = "active"
    dimScreen = ""
    onTime = false;
    crowded = false;
    showModal = false;
    submission = false;
    closeModal() {

    }
    openModal() {
        if(!this.submission) {
            this.showModal = true;
        } else {
            alert("You only get 1 feedback per search");
        }
    }
    changeCrowded(value) {
        this.crowded = value;
    }
    changeTime(value) {
        this.onTime = value;
    }
    recordResults() {
        console.log("On time:", this.onTime, "Crowded:", this.crowded);
        this.tokens++;
        Global.tokens++;
        this.submission = true;
    }
}
