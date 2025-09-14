import { Component } from '@angular/core';
import { StravaAuthService } from '../services/strava-auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  constructor(private stravaAuthService: StravaAuthService) {}

  loginWithStrava(): void {
    this.stravaAuthService.redirectToStravaAuth();
  }
} 