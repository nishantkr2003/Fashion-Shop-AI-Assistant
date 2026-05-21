export async function validateSession() {
  try {
    const res = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/profile`,

      {
        credentials: "include",
      },
    );

    return res.ok;
  } catch {
    return false;
  }
}
