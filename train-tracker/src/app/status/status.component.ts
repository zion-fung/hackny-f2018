import { Component, OnInit } from '@angular/core';
import { Global } from "../global";

@Component({
    selector: 'app-status',
    templateUrl: './status.component.html',
    styleUrls: ['./status.component.css']
})
export class StatusComponent implements OnInit {
    data = [];
    constructor() { }

    ngOnInit() {
        // Initialize data with objects of keys: predicted, scheculed, and difference
    }
    test() {
        console.log("Hello world");
    }
    modalStatus = "active"
    dimScreen = ""
    onTime = false;
    crowded = false;
    closeModal() {
        this.modalStatus = ""
        this.dimScreen = ""
    }
    openModal() {
        this.modalStatus = "active"
        this.dimScreen = "active"
    }
    changeCrowded(value) {
        this.crowded = value;
    }
    changeTime(value) {
        this.onTime = value;
    }
    recordResults() {
        
    }
}
