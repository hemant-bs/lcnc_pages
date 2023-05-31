import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['app.component.css']
})
export class AppComponent {
  name: string;
  email: string;
  subscribe: boolean;
  favoriteColor: string;
  imageUrl: string;
  submitted: boolean;

  constructor() {
    this.name = '';
    this.email = '';
    this.subscribe = false;
    this.favoriteColor = '';
    this.submitted = false;
    this.imageUrl = 'https://mdbootstrap.com/img/Others/documentation/img%20(7)-mini.jpg';
  }

  submitForm() {
    this.submitted = true;
  }
}
