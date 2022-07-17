import { Component } from '@angular/core';
import { StorageService } from './_services/storage.service';
import { AuthService } from './_services/auth.service';
import { MenuItem } from 'primeng/api';
import { Router } from '@angular/router';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  private roles: string[] = [];
  isLoggedIn = false;
  showAdminBoard = false;
  showModeratorBoard = false;
  username?: string;
  items: MenuItem[] = [];
  isAdmin = false;
  constructor(private storageService: StorageService, private authService: AuthService, private router: Router ) { }


  ngOnInit(): void {
    this.isLoggedIn = this.storageService.isLoggedIn();

    if (this.isLoggedIn) {
      const user = this.storageService.getUser();

      this.username = user.username;
      this.isAdmin = user.username == 'admin';
    }
   
      this.items = [
        {
          label: 'Home',
          icon: 'pi pi-fw pi-home',
          routerLink: ['/home'],
          visible: this.isLoggedIn,
        },
        {
          label: 'Login',
          icon: 'pi pi-fw pi-user',
          routerLink: ['/login'],
          visible: !this.isLoggedIn,
        },
        {
          label: 'Admin',
          icon: 'pi pi-fw pi-cog',
          routerLink: ['/admin'],
          visible: this.isLoggedIn && this.isAdmin,
        },
        {
          label: 'Logout',
          icon: 'pi pi-fw pi-power-off',
          visible: this.isLoggedIn,
          command: () => {
            this.logout();
          },
        },
      ];
  }

  logout(): void {
    this.storageService.clean();
    
    this.router.navigate(['/login']);
  }
}
