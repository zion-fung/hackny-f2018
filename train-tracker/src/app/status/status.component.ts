import { Component, OnInit } from '@angular/core';
import { Global } from "../global";
import { HttpClient } from '@angular/common/http';
import { Router } from "@angular/router";
import { Outside } from "../../outside";

@Component({
    selector: 'app-status',
    templateUrl: './status.component.html',
    styleUrls: ['./status.component.css']
})
export class StatusComponent implements OnInit {
    
    data = [];
    constructor(private http: HttpClient, private router: Router) { }
    tokens = 0;
    showInputs = true;
    start_html = "";
    end_html = "";
    ngOnInit() {
        // this.start_html = document.querySelector("#start").innerHTML;
        // this.end_html = document.querySelector("#end").innerHTML;
        // this.end_html = document.getElementsByClassName("end")[0].innerHTML;
        // this.start_html = document.getElementsByClassName("start")[0].innerHTML;
        document.getElementsByClassName("end")[0].innerHTML = "";
        document.getElementsByClassName("start")[0].innerHTML = "";
        this.tokens = Global.tokens;
        console.log("Sending feed id:", Global.line_feeds[Global.train]);
        console.log("Sending station id:", Global.origin);
        // Initialize data with objects of keys: predicted, scheculed, and difference
        this.data = Global.data.slice(0);
        this.showInputs = false;
    }
    goBack() {
        // document.querySelector("#start").innerHTML = this.start_html;
        // document.querySelector("#end").innerHTML = this.end_html;
        // document.getElementsByClassName("end")[0].innerHTML = this.end_html;
        // document.getElementsByClassName("start")[0].innerHTML = this.start_html;
        this.router.navigate(["/home"]);
        window.location.reload();   
        // this.http.get("http://localhost:5000/").subscribe(
        //     data => {

        //     }, error => {

        //     }
        // )
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
    train_id = ""
    closeModal() {

    }
    openModal(data) {
        if(!this.submission) {
            this.showModal = true;
        } else {
            alert("You only get 1 feedback per search");
        }
        this.train_id = data;
        console.log("Train id:", data);
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
        const timeBody = {
            "train_id": Number(this.train_id),
            "status": this.onTime
        };
        const crowdedBody = {
            "train_id": Number(this.train_id),
            "status": !this.crowded
        };
        // console.log(timeBody);
        // console.log(crowdedBody);
        this.http.post("http://localhost:5000/train-status", timeBody).subscribe(
            result => {
                console.log("Train id:", this.train_id, "now at", result);
            }, error => {
                console.log("Error:", error);
            }
        );
        this.http.post("http://localhost:5000/train-status", crowdedBody).subscribe(
            result => {
                console.log("Train id:", this.train_id, "now at", result);
            }, error => {
                console.log("Error:", error);
            }
        );
        this.updateData();
    }
    updateData() {
        this.http.post("http://localhost:5000/station-line-info", {"feed_id": Global.line_feeds[Global.train], "station_id": Global.origin}).subscribe(
            data => {
                // Clear old data first
                Global.data = [];
                for(const i of Object.keys(data)) {
                    Global.data.push(data[i]);
                }
                this.data = Global.data.slice(0);
            }, error => {
                alert("Error processing data");
            }
        )
    }
}
