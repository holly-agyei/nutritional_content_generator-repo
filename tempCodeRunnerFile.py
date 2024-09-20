
        results = f"Error: {str(e)}"
    
    # Store results in the session and redirect to home
    session['results'] = results
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
