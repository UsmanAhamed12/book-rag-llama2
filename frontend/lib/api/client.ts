const API_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_URL) {
  throw new Error(
    "NEXT_PUBLIC_API_URL is not configured",
  );
}

export class ApiError extends Error {
  status: number;

  constructor(
    message: string,
    status: number,
  ) {
    super(message);

    this.name = "ApiError";
    this.status = status;
  }
}

function handleUnauthorized(): void {
  if (typeof window === "undefined") {
    return;
  }

  const token =
    localStorage.getItem(
      "access_token",
    );

  /*
   * If there is no stored token, this may simply be
   * a failed login attempt. Do not force a redirect.
   */
  if (!token) {
    return;
  }

  localStorage.removeItem(
    "access_token",
  );

  /*
   * Avoid repeatedly redirecting while already
   * on the login page.
   */
  if (
    window.location.pathname !==
    "/login"
  ) {
    window.location.replace(
      "/login",
    );
  }
}

async function getErrorMessage(
  response: Response,
): Promise<string> {
  let message =
    response.status >= 500
      ? "The server could not complete your request. Please try again."
      : "Request failed";

  try {
    const body: unknown =
      await response.json();

    if (
      typeof body === "object" &&
      body !== null &&
      "detail" in body
    ) {
      const detail = (
        body as {
          detail?: unknown;
        }
      ).detail;

      if (
        typeof detail ===
        "string"
      ) {
        message = detail;
      } else if (
        Array.isArray(detail) &&
        detail.length > 0 &&
        typeof detail[0] === "object" &&
        detail[0] !== null &&
        "msg" in detail[0] &&
        typeof detail[0].msg === "string"
      ) {
        message = detail[0].msg;
      }
    }
  } catch {
    // Response was not JSON.
  }

  return message;
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  let response: Response;

  try {
    response = await fetch(
      `${API_URL}${path}`,
      {
        ...options,

        headers: {
          Accept:
            "application/json",
          ...options.headers,
        },
      },
    );
  } catch {
    throw new ApiError(
      "Unable to connect to the server.",
      0,
    );
  }

  if (!response.ok) {
    const message =
      await getErrorMessage(
        response,
      );

    if (
      response.status === 401
    ) {
      handleUnauthorized();
    }

    throw new ApiError(
      message,
      response.status,
    );
  }

  /*
   * Some successful DELETE endpoints may
   * eventually return 204 No Content.
   */
  if (
    response.status === 204
  ) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}
