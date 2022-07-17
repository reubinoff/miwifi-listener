import { Component, OnInit } from '@angular/core';
import { StorageService } from '../_services/storage.service';
import { UserService } from '../_services/user.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  users: string[] = [];
  selectedUser: string = "";
  errorMessage = '';
  username: string = "";

  form: any = {
    username: null,
    duration: null
  };
  constructor(private userService: UserService, private storageService: StorageService) { }



  ngOnInit(): void {
    this.username = this.storageService.getUser().username;
    this.form.username = this.username;

   
  }

    onSubmit(): void {
    const { username, password } = this.form;

    // this.authService.login(username, password).subscribe({
    //   next: data => {
    //     this.storageService.saveUser(data);
    //     console.log(data);
    //     this.isLoginFailed = false;
    //     this.isLoggedIn = true;
    //     this.username = this.storageService.getUser().username;
    //     this.reloadPage();
    //   },
    //   error: err => {
    //     this.errorMessage = err.error.message;
    //     this.isLoginFailed = true;
    //   }
    // });
  }
}
