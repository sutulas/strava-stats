import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { QueryFormComponent } from './query-form/query-form.component';
import { DataOverviewComponent } from './data-overview/data-overview.component';
import { NavigationComponent } from './navigation/navigation.component';
import { LoadingSpinnerComponent } from './shared/loading-spinner/loading-spinner.component';
import { ChartDisplayComponent } from './chart-display/chart-display.component';
import { LoginComponent } from './login/login.component';
import { TokenCallbackComponent } from './token-callback/token-callback.component';
import { ProfileComponent } from './profile/profile.component';
import { WeeklyPaceChartComponent } from './shared/weekly-pace-chart/weekly-pace-chart.component';

const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'token', component: TokenCallbackComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'query', component: QueryFormComponent },
  { path: 'overview', component: DataOverviewComponent },
];

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    QueryFormComponent,
    DataOverviewComponent,
    NavigationComponent,
    LoadingSpinnerComponent,
    ChartDisplayComponent,
    LoginComponent,
    TokenCallbackComponent,
    ProfileComponent,
    WeeklyPaceChartComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule.forRoot(routes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { } 