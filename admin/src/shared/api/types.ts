/**
 * API javob shakli — Menu Mate backend'i har javobda aynan shu formatni qaytaradi.
 * `apps/shared/utils/custom_response.py` va `apps/shared/exceptions/custom_exceptions.py`
 * bilan bir xil kontrakt.
 */

/** Muvaffaqiyatli javob. `data` maydoni endpoint'ga qarab har xil turda bo'ladi. */
export interface ApiSuccess<T> {
  success: true;
  id: string;
  message: string;
  data: T;
}

/** Server yoki client-side xato. */
export interface ApiFailure {
  success: false;
  id: string;
  message: string;
  errors?: Record<string, unknown>;
}

/** DRF `PageNumberPagination` sxemasi. */
export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

/**
 * `ApiError` — HTTP xatoni yagona shaklga keltiruvchi tashuvchi.
 *
 * Frontend joylarda `try / catch (err)` da `err instanceof ApiError` bilan
 * tekshiriladi. Kod tozaligini ta'minlaydi.
 */
export class ApiError extends Error {
  public readonly id: string;
  public readonly status: number;
  public readonly fieldErrors: Record<string, unknown> | undefined;

  constructor(params: {
    id: string;
    message: string;
    status: number;
    fieldErrors?: Record<string, unknown>;
  }) {
    super(params.message);
    this.name = 'ApiError';
    this.id = params.id;
    this.status = params.status;
    this.fieldErrors = params.fieldErrors;
  }

  /** So'rov tarmoq muammosi tufayli yubormay tushdi. */
  static network(): ApiError {
    return new ApiError({
      id: 'NETWORK_ERROR',
      message: 'Tarmoq bilan aloqa yoq. Internetni tekshiring.',
      status: 0,
    });
  }

  /** Server javob berdi lekin format kutilganidan boshqacha. */
  static unknown(status: number): ApiError {
    return new ApiError({
      id: 'UNKNOWN_ERROR',
      message: 'Kutilmagan xatolik. Keyinroq urinib koring.',
      status,
    });
  }
}
