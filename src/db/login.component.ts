import { Component } from '@angular/core';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
})
export class LoginComponent {
  email = '';
  senha = '';
  errorMessage = '';

  constructor(private authService: AuthService) {}

  onLogin() {
    this.authService.login(this.email, this.senha).subscribe(
      (response) => {
        console.log('Login bem-sucedido:', response);
        // Redirecione ou salve o estado do usuário
      },
      (error) => {
        this.errorMessage = error.error.message || 'Erro no login';
        console.error('Erro no login:', error);
      }
    );
  }
}
