import { Injectable } from '@angular/core'
import {
  HttpEvent,
  HttpInterceptor,
  HttpHandler,
  HttpRequest,
  HttpErrorResponse
} from '@angular/common/http'

import { Observable, throwError } from 'rxjs'
import { catchError } from 'rxjs/operators'

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {

  intercept(
    req: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {

    return next.handle(req).pipe(

      catchError((error: HttpErrorResponse) => {

        let apiError = null

        if (error.error) {

          // FastAPI error may be wrapped in "detail"
          apiError = error.error.detail ?? error.error

        }

        if (!apiError) {

          apiError = {
            status: "FAILED",
            errorCode: "UNKNOWN",
            transactionId: null,
            message: "Unexpected error occurred"
          }

        }

        // console.error("API ERROR:", apiError)

        return throwError(() => apiError)

      })

    )
  }
}