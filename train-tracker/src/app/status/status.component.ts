import { Component, OnInit } from '@angular/core';

@Component({
    selector: 'app-status',
    templateUrl: './status.component.html',
    styleUrls: ['./status.component.css']
})
export class StatusComponent implements OnInit {

    constructor() { }

    ngOnInit() {
        
    }
    test() {
        console.log("Hello world");
    }
    modalStatus = "active"
    dimScreen = ""
    closeModal() {
        this.modalStatus = ""
        this.dimScreen = ""
    }
    openModal() {
        this.modalStatus = "active"
        this.dimScreen = "active"
    }
}
