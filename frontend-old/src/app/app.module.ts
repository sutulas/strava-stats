import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';

// Angular Material Modules
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatBadgeModule } from '@angular/material/badge';
import { MatMenuModule } from '@angular/material/menu';
import { MatDividerModule } from '@angular/material/divider';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatChipsModule } from '@angular/material/chips';
import { MatExpansionModule } from '@angular/material/expansion';

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
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule.forRoot(routes),
    // Angular Material Modules
    MatToolbarModule,
    MatSidenavModule,
    MatListModule,
    MatIconModule,
    MatButtonModule,
    MatCardModule,
    MatInputModule,
    MatFormFieldModule,
    MatBadgeModule,
    MatMenuModule,
    MatDividerModule,
    MatProgressSpinnerModule,
    MatChipsModule,
    MatExpansionModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { } 